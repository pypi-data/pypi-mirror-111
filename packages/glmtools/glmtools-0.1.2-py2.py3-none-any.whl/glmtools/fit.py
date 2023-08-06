# vim: set expandtab ts=4 sw=4:

import numpy as np
import multiprocessing as mp
from functools import partial
from scipy import ndimage, optimize
from anamnesis import AbstractAnam, register_class

from . import util


class AbstractModelFit(AbstractAnam):
    """
    Class for performing a GLM fit and storing results
    """

    hdf5_outputs = ['betas', 'copes', 'varcopes', 'coapes', 'fstats',
                    'beta_dimlabels', 'cope_dimlabels',
                    'good_observations', 'dof_error', 'dof_model',
                    'ss_total', 'ss_model', 'ss_error', 'time_dim',
                    'regressor_names', 'contrast_names', 'ftest_names']

    def __init__(self, design=None, data_obj=None, standardise_data=False, tags=None, fit_args=None):
        """Computes a GLM fit on a defined model and a dataset.

        Parameters
        ----------

        design : GLMDesign instance
            Design object defined by GLMDesign

        data_obj : TrialGLMData or ContinuousGLMData instance
            Data object defined by TrialGLMData or ContinuousGLMData

        standardise_data : boolean (optional, default=False)
            Boolean flag indicating whether to z-transform input data prior to
            fitting.

        Returns
        -------
            GLMFit instance

        """
        AbstractAnam.__init__(self)

        # In case we're initialising in a classmethod (probably a better solution for this somewhere...)
        if design is None or data_obj is None:
            return

        design.sanity_check()

        # Collapse all dimensions apart from the observations
        # Parameters and COPEs are returned in the original data dimensions at the end
        data = data_obj.get_2d_data()

        if standardise_data:
            data = util.standardise_data(data)
            self.is_standardised = True
        else:
            self.is_standardised = False

        # Store a copy of the design matrix
        self._design = design
        self.design_matrix = design.design_matrix
        self.regressor_list = design.regressor_list

        # Compute number of valid observations (observations with NaNs are ignored)
        self.good_observations = np.isnan(data.sum(axis=1)) == False  # noqa: E712

        # Adjust degrees of freedom for bad samples
        n_bad_samples = design.num_observations - self.good_observations.sum()
        self.dof_error = design.dof_error - n_bad_samples
        self.dof_model = self.dof_error - np.linalg.matrix_rank(self.design_matrix)

        # Run the actual fit
        self.compute_fit(design.design_matrix[self.good_observations, :],
                         data[self.good_observations, :],
                         design.contrasts,
                         fit_args=fit_args)

        # Set Absolue COPES
        self.coapes = np.abs(self.copes)

        # Compute sum squares for data and residuals
        self.ss_total = np.sum(np.power(data[self.good_observations, :], 2), axis=0)
        self.ss_model = np.sum(np.power(self.get_prediction(), 2), axis=0)
        self.ss_error = np.sum(np.power(self.get_residuals(data[self.good_observations, :]), 2), axis=0)

        # Compute F-tests if defined
        if design.ftests is None:
            self.fstats = None
        else:
            self.fstats = np.zeros((design.num_ftests, data.shape[1]))
            self.get_resid_dots(data[self.good_observations, :])

            for jj in range(design.num_ftests):
                cont_ind = design.ftests[jj, :].astype(bool)
                C = design.contrasts[cont_ind, :]
                D = design.design_matrix

                a = np.linalg.pinv(D.T.dot(D))
                b = np.linalg.pinv(np.linalg.multi_dot([C, a, C.T]))

                for ii in range(data.shape[1]):

                    B = self.betas[:, ii]
                    c = np.linalg.multi_dot([B.T, C.T, b, C, B])

                    num = c / np.linalg.matrix_rank(C)
                    denom = self.resid_dots[ii] / self.dof_error

                    self.fstats[jj, ii] = num / denom

        # Restore original data shapes
        self.betas = data_obj.unsquash_array(self.betas)
        self.copes = data_obj.unsquash_array(self.copes)
        self.coapes = data_obj.unsquash_array(self.coapes)
        self.varcopes = data_obj.unsquash_array(self.varcopes)
        if self.fstats is not None:
            self.fstats = data_obj.unsquash_array(self.fstats)

        self.ss_total = data_obj.unsquash_array(self.ss_total[None, :])
        self.ss_error = data_obj.unsquash_array(self.ss_error[None, :])
        self.ss_model = data_obj.unsquash_array(self.ss_model[None, :])

        self.regressor_names = design.regressor_names
        self.contrast_names = design.contrast_names
        self.ftest_names = design.ftest_names
        if 'time_dim' in data_obj.info and data_obj.info['time_dim'] is not None:
            self.time_dim = data_obj.info['time_dim']
        else:
            self.time_dim = None
        self.tags = tags

        self.beta_dimlabels = list(('Regressors',
                                    *data_obj.info['dim_labels'][1:]))
        self.cope_dimlabels = list(('Contrasts',
                                    *data_obj.info['dim_labels'][1:]))
        self.tstat_dimlabels = list(('Contrasts',
                                     *data_obj.info['dim_labels'][1:]))

    def compute_betas(self, design_matrix, data, fit_args=None):

        raise NotImplementedError('This is an abstract class, please use OLSModel')

    def get_prediction(self):

        return self.design_matrix[self.good_observations, :].dot(self.betas)

    def get_residuals(self, data):

        return data - self.get_prediction()

    def get_studentized_residuals(self, data):

        return self.get_residuals(data) / self.mse / np.sqrt(1 - self._design.leverage)[:, None]

    def get_resid_dots(self, data):
        resid = self.get_residuals(data)
        self.resid_dots = np.einsum('ij,ji->i', resid.T, resid)

    def get_tstats(self,
                   varcope_smoothing=None, smoothing_window=np.hanning,
                   smooth_dims=None, sigma_hat=None):
        """Computes t-statistics from COPEs in a fitted model, may add optional
        temporal varcope smoothing.

        Parameters
        ----------

        varcope_smoothing : {None, int} (optional, default=None)
            Optional window length for varcope smoothing of time dimension. The
            default is no smoothing as indicated by None.

        smoothing_window : {np.hanning,np.bartlett,np.blackman,np.hamming} default=np.hanning
            One of numpys window functions to apply during smoothing. Ignored
            if varcope_smoothing=None

        Returns
        -------

        ndarray
            Array containing t-statistic estimates

        """
        return get_tstats(self.copes, self.varcopes.copy(),
                          varcope_smoothing=varcope_smoothing, smoothing_window=np.hanning,
                          smooth_dims=None, sigma_hat=sigma_hat)

    def project_range(self, contrast, nsteps=2, values=None, mean_ind=0):
        """Get model prediction for a range of values across one regressor."""

        steps = np.linspace(self.design_matrix[:, contrast].min(),
                            self.design_matrix[:, contrast].max(),
                            nsteps)
        pred = np.zeros((nsteps, *self.betas.shape[1:]))

        # Run projection
        for ii in range(nsteps):
            if nsteps == 1:
                coeff = 0
            else:
                coeff = steps[ii]
            pred[ii, ...] = self.betas[mean_ind, ...] + coeff*self.betas[contrast, ...]

        # Compute label values
        if nsteps > 1:
            scale = self.regressor_list[contrast].values_orig
            llabels = np.linspace(scale.min(), scale.max(), nsteps)
        else:
            llabels = ['Mean']

        return pred, llabels

    @property
    def num_observations(self):

        return self.design_matrix.shape[0]

    @property
    def num_regressors(self):

        return self.betas.shape[0]

    @property
    def tstats(self):
        return get_tstats(self.copes, self.varcopes)

    @property
    def num_contrasts(self):

        return self.copes.shape[0]

    @property
    def num_tests(self):

        return self.betas.shape[1]

    @property
    def mse(self):

        return self.ss_error / self.dof_error

    @property
    def r_square(self):

        return 1 - (self.ss_error / self.ss_total)

    @property
    def cooks_distance(self, data):
        """https://en.wikipedia.org/wiki/Cook%27s_distance"""

        raise RuntimeError

        # Leverage per observation
        hat_diag = self._design.leverage
        term2 = hat_diag / ((1 - hat_diag)**2)

        return term2

    @property
    def log_likelihood(self):

        raise NotImplementedError('This is an abstract class')

    @property
    def aic(self):
        return self.log_likelihood() + 2*self.num_regressors

    @property
    def bic(self):
        return self.log_likelihood() + (self.num_regressors*np.log(self.num_observations))

    @classmethod
    def load_from_hdf5(cls, hdfpath):

        # This function will be removed soon but keeping it for reference atm.
        # Raise a warning if someone happens to use it
        raise DeprecationWarning('Please use Anamnesis API instead!')

        ret = cls()

        import h5py
        f = h5py.File(hdfpath)

        ret.betas = f['OLSModel/betas'][...]
        ret.copes = f['OLSModel/copes'][...]
        ret.coapes = f['OLSModel/coapes'][...]
        ret.varcopes = f['OLSModel/varcopes'][...]

        ret.ss_total = f['OLSModel/ss_total'][...]
        ret.ss_error = f['OLSModel/ss_error'][...]
        ret.ss_model = f['OLSModel/ss_model'][...]

        if 'fstats' in f['OLSModel'].keys():
            ret.fstats = f['OLSModel/fstats'][...]
            ret.ftest_names = list(f['OLSModel/ftest_names'][...])
        else:
            ret.fstats = None
            ret.ftest_names = None

        ret.regressor_names = list(f['OLSModel/regressor_names'][...])
        ret.contrast_names = list(f['OLSModel/contrast_names'][...])
        ret.beta_dimlabels = tuple(f['OLSModel/beta_dimlabels'][...])
        ret.cope_dimlabels = tuple(f['OLSModel/cope_dimlabels'][...])

        ret.good_observations = f['OLSModel/good_observations'][...]

        ret.dof_error = f['OLSModel'].attrs['dof_error']
        ret.dof_model = f['OLSModel'].attrs['dof_model']

        ret.time_dim = f['OLSModel'].attrs['time_dim']

        return ret


register_class(AbstractModelFit)


def _get_varcope_thresh2(vc, factor=2):
    from sklearn.mixture import GaussianMixture
    vc = np.log(vc.reshape(-1, 1))
    gm = GaussianMixture(n_components=2, random_state=0).fit(vc)
    x = np.linspace(vc.min(), vc.max(), 100000)
    preds = gm.predict(x.reshape(-1, 1))
    thresh = np.where(np.diff(preds) != 0)[0][0]
    thresh = x[thresh]
    return np.exp(thresh)*factor


def _get_varcope_thresh(vc, factor=3):
    vc = np.log(vc.reshape(-1, 1))
    thresh = np.max(vc)-factor
    return np.exp(thresh)


def varcope_hat_correction(vc, factor=3):
    thresh = _get_varcope_thresh(vc, factor=factor)
    vc = vc.copy()
    vc[vc < thresh] = thresh
    return vc


def get_tstats(copes, varcopes,
               varcope_smoothing=None, smoothing_window=np.hanning,
               smooth_dims=None, sigma_hat='auto', sigma_factor=3):
    """Computes t-statistics from COPEs in a fitted model, may add optional
    temporal varcope smoothing.

    Parameters
    ----------

    varcope_smoothing : {None, int} (optional, default=None)
        Optional window length for varcope smoothing of time dimension. The
        default is no smoothing as indicated by None.

    smoothing_window : {np.hanning,np.bartlett,np.blackman,np.hamming} default=np.hanning
        One of numpys window functions to apply during smoothing. Ignored
        if varcope_smoothing=None

    Returns
    -------

    ndarray
        Array containing t-statistic estimates

    """

    if sigma_hat == 'auto':
        varcopes = varcope_hat_correction(varcopes, factor=sigma_factor)
    elif sigma_hat is not None:
        varcopes[varcopes < sigma_hat] = sigma_hat

    if varcope_smoothing == 'avg':

        dim_len = varcopes.shape[smooth_dims]
        varcopes = varcopes.mean(smooth_dims)
        varcopes = np.expand_dims(varcopes, smooth_dims)

        denom = np.repeat(np.sqrt(varcopes), dim_len, axis=smooth_dims)

    elif varcope_smoothing is not None and varcope_smoothing > 0 and isinstance(smooth_dims, int):
        # Create window normalised to have area of 1
        # TODO: probably redundant with newer method below
        w = smoothing_window(varcope_smoothing)
        w = w / w.sum()

        func = lambda m: np.convolve(m, w, mode='same')  # noqa E731
        varcope = np.apply_along_axis(func, smooth_dims, arr=varcopes)

        denom = np.sqrt(varcope)

    elif varcope_smoothing is not None and len(smooth_dims) > 1:
        sigma = np.zeros((varcopes.ndim,))
        sigma[np.array(smooth_dims)] = varcope_smoothing
        denom = np.sqrt(ndimage.gaussian_filter(varcopes, sigma))

    else:
        denom = np.sqrt(varcopes)

    # Compute t-values
    # run this in where to avoid RunTimeWarnings
    tstats = np.where(np.isnan(denom) == False, copes / denom, np.nan)  # noqa E712

    return tstats

# -------------------------------------------------------------------------
# OLS Implementation


def _get_prediction(design_matrix, betas):
    return design_matrix.dot(betas)


def _get_residuals(design_matrix, betas, data):
    return data - _get_prediction(design_matrix, betas)


def ols_fit(design_matrix, data, contrasts, method='pinv'):
    """Fit a Ordinary Least Squares fit."""

    if method == 'pinv':
        betas = compute_betas_pinv(design_matrix, data)
    elif method == 'numpy_lstsq':
        betas = compute_betas_numpy_lstsq(design_matrix, data)

    copes = compute_ols_contrasts(contrasts, betas)

    varcopes = compute_ols_varcopes(design_matrix, data, contrasts, betas)

    return betas, copes, varcopes


def compute_betas_pinv(design_matrix, data):
    # Invert design matrix
    design_matrix_inv = np.linalg.pinv(design_matrix)

    # Estimate betas
    return design_matrix_inv.dot(data)


def compute_betas_numpy_lstsq(design_matrix, data):
    b, residuals, rank, s = np.linalg.lstsq(design_matrix, data)
    return b


def compute_ols_contrasts(contrasts, betas):
    # Compute contrasts
    copes = contrasts.dot(betas)

    return copes


def compute_ols_varcopes(design_matrix, data, contrasts, betas):

    # Compute varcopes
    varcopes = np.zeros((contrasts.shape[0], data.shape[1]))

    # Compute varcopes
    residue_forming_matrix = np.linalg.pinv(design_matrix.T.dot(design_matrix))
    var_forming_matrix = np.diag(np.linalg.multi_dot([contrasts,
                                                     residue_forming_matrix,
                                                     contrasts.T]))

    # This is equivalent to >> np.diag( resid.T.dot(resid) )
    resid = _get_residuals(design_matrix, betas, data)
    resid_dots = np.einsum('ij,ji->i', resid.T, resid)
    del resid
    dof_error = data.shape[0] - np.linalg.matrix_rank(design_matrix)
    V = resid_dots / dof_error
    varcopes = var_forming_matrix[:, None] * V[None, :]

    return varcopes


class OLSModel(AbstractModelFit):

    def compute_fit(self, design_matrix, data, contrasts, fit_args=None):

        b, c, v = ols_fit(design_matrix, data, contrasts)
        self.betas = b
        self.copes = c
        self.coapes = np.abs(c)
        self.varcopes = v

    def log_likelihood(self):

        ll = - self.num_observations / 2.
        ll = ll * np.log(self.ss_error)
        return ll + (1 + np.log(2*np.pi)/self.num_observations)


register_class(OLSModel)

# ---------------------------------------------------------
# sklearn functions


def skl_fit(design_matrix, data, contrasts, estimator=None):
    """Fit using a paramatrised SK-Learn object."""

    if estimator is None:
        from sklearn import linear_model
        estimator = linear_model.LinearRegression

    betas, skm = _fit_sk(estimator, design_matrix, data)

    copes, coapes = compute_ols_contrasts(contrasts, betas)

    varcopes = compute_ols_varcopes(design_matrix, data, contrasts, betas)

    return betas, copes, varcopes, skm


class SKLModel(AbstractModelFit):

    def compute_fit(self, design_matrix, data, fit_args=None):
        from sklearn import linear_model

        if fit_args is None:
            fit_args = {'lm': 'LinearRegression'}

        # Always assume that the design matrix has this right
        if 'fit_intercept' not in fit_args:
            fit_args['fit_intercept'] = False

        self.fit_args = fit_args.copy()

        # Actual model fit
        rtype = fit_args.pop('lm')
        batch = fit_args.pop('batch', 'sklearn')
        njobs = fit_args.pop('njobs', 1)
        reg = getattr(linear_model, rtype)

        if rtype == 'RANSACRegressor':
            # We need to pass in a base estimator
            base_estimator = linear_model.LinearRegression(**fit_args)
            reg = reg(base_estimator=base_estimator)
        else:
            reg = reg(**fit_args)

        if batch == 'sklearn':
            # Use sklearns internal batching - this considers all features
            # together. For instance, outliers will be detected across the
            # whole dataset

            self.betas, self.skm = _fit_sk(reg, design_matrix, data)

        else:
            # Use an external batching loop - this will consider each
            # regression as a separate entity. For instance, outliers are
            # detected independantly in each 'feature'

            args = [(reg, design_matrix, data[:, ii]) for ii in range(data.shape[1])]

            import multiprocessing as mp
            p = mp.Pool(processes=njobs)

            res = p.starmap(_fit_sk, args)

            self.betas = np.concatenate(([r[0] for r in res]), axis=1)
            self.skm = [r[1] for r in res]


register_class(SKLModel)


class SKLModel2(AbstractModelFit):

    def compute_fit(self, design_matrix, data, contrasts, fit_args=None):
        from sklearn import linear_model
        if fit_args is None:
            skl_fitter = linear_model.LinearRegression()
        else:
            skl_fitter = fit_args['lm']

        self.betas, self.skm = _fit_sk(skl_fitter, design_matrix, data)

        self.varcopes = compute_ols_varcopes(design_matrix, data, contrasts, self.betas)


def _fit_sk(reg, design_matrix, data):

    skm = reg.fit(X=design_matrix, y=data)
    if hasattr(skm, 'coef_'):
        betas = skm.coef_.T
    elif hasattr(skm, 'estimator_') and hasattr(skm.estimator_, 'coef_'):
        betas = skm.estimator_.coef_.T

    if betas.ndim == 1:
        betas = betas[:, None]

    return betas, skm


# ---------------------------------------------------------
# Flame1 functions


def logbetafunctionnew(x, y, z, S):
    iU = np.diag(1 / (S + np.exp(x)))
    ziUz = z.T.dot(iU).dot(z)
    gam = np.linalg.inv(ziUz).dot(z.T).dot(iU).dot(y)
    ret = -(0.5*np.log(np.linalg.det(iU)) - 0.5*np.log(np.linalg.det(ziUz)) -
            0.5*(y.T.dot(iU).dot(y) - gam.T.dot(ziUz).dot(gam)))
    return ret


def _run_flame1(y, z, S, contrasts, fixed=False):
    """Solve GLM y=z*gam+e where e~N(0, beta+diag(S)) using FLAME1.

    Fast-posterior approximation using section 3.5 & 10.7 of
    https://www.fmrib.ox.ac.uk/datasets/techrep/tr03mw1/tr03mw1.pdf
    """

    opt_func = partial(logbetafunctionnew, y=y, z=z, S=S)

    if fixed:
        beta = 0
    else:
        # Brent's algorithm solving eqn 45
        res = optimize.minimize_scalar(opt_func, method='brent')
        if res.success is False:
            print('Brent Fail!')
        beta = np.exp(res.x)

    iU = np.diag((1 / (S + beta)))

    covgam = np.linalg.pinv(z.T.dot(iU).dot(z))
    gam = covgam.dot(z.T).dot(iU).dot(y)

    cope = contrasts.dot(gam)
    varcope = contrasts.dot(covgam).dot(contrasts.T)
    return gam, cope, varcope


def flame1(design_matrix, data, S, contrasts, fixed=False, nprocesses=1):

    if data.ndim == 1:
        data = data[:, np.newaxis]
    if S.ndim == 1:
        S = S[:, np.newaxis]

    if np.any(S < 0):
        print('NEGATIVE VARCOPES!!')

    p = mp.Pool(nprocesses)

    args = [(data[:, ii], design_matrix, S[:, ii], contrasts) for ii in range(data.shape[1])]

    res = p.starmap(_run_flame1, args, total=len(args))

    p.close()

    betas = np.vstack([r[0] for r in res])
    copes = np.vstack([r[1] for r in res])
    varcopes = np.vstack([r[2] for r in res])

    return betas, copes, varcopes
