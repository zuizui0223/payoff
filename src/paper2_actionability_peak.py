"""Exact zero-wait-cost information/actionability optimum for Paper 2.

For future cue accuracy q(t)=q0 + dq*(1-exp(-alpha*t)), retained
actionability r(t)=exp(-beta*t), state loss scale S and prior choice
cost B, maximize optional positive net opportunity

    N(t) = r(t) * (S*q(t)-B)

over t >= 0, also allowing the actor to take a zero-payoff outside action.

The popular t*=log(1+alpha/beta)/alpha is only obtained in the
threshold-normalized case S*q0=B. Results in this module are elementary
calculus, not new ecological theorems or estimated fitness.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, log


@dataclass(frozen=True)
class ActionabilityPeak:
    q0: float
    dq: float
    alpha: float
    beta: float
    loss_scale: float
    baseline_loss: float

    def __post_init__(self):
        vals=(self.q0,self.dq,self.alpha,self.beta,self.loss_scale,self.baseline_loss)
        if not all(isfinite(v) for v in vals):
            raise ValueError("Parameters must be finite")
        if not (0.5 <= self.q0 <= 1 and 0 <= self.dq <= 1-self.q0+1e-15):
            raise ValueError("Cue reliability must start in [0.5,1] and not exceed 1")
        if self.alpha<=0 or self.beta<=0 or self.loss_scale<=0 or self.baseline_loss<0:
            raise ValueError("Positive learning/decay rates, positive scale, nonnegative loss required")

    @property
    def asymptotic_gross(self)->float:
        return self.loss_scale*(self.q0+self.dq)-self.baseline_loss

    @property
    def learning_amplitude(self)->float:
        return self.loss_scale*self.dq

    def cue_accuracy(self,t:float)->float:
        if not isfinite(t) or t<0:
            raise ValueError("time must be finite and >=0")
        return self.q0+self.dq*(1-exp(-self.alpha*t))

    def net(self,t:float)->float:
        return exp(-self.beta*t)*(self.loss_scale*self.cue_accuracy(t)-self.baseline_loss)

    def derivative(self,t:float)->float:
        if not isfinite(t) or t<0:
            raise ValueError("time must be finite and >=0")
        return exp(-self.beta*t)*(
            (self.alpha+self.beta)*self.learning_amplitude*exp(-self.alpha*t)
            -self.beta*self.asymptotic_gross
        )

    def optimum(self)->dict:
        """Global nonnegative optimum for free/optional informational action.

        If asymptotic gross gain <=0, every finite t has nonpositive gain,
        and the zero-payoff action is optimal. If positive, derivative
        changes sign at most once and the optimum is at t=0 or the
        positive stationary point.
        """
        a=self.asymptotic_gross
        d=self.learning_amplitude
        if a<=0:
            return {"regime":"NO_POSITIVE_INFORMATION_RETURN",
                    "optimal_wait_time":None,"optimal_net_value":0.0,
                    "interior_stationary_point":None}
        ratio=(self.alpha+self.beta)*d/(self.beta*a)
        stationary=log(ratio)/self.alpha if ratio>0 else None
        if ratio<=1.0:
            best=0.0
            regime="COMMIT_IMMEDIATELY"
        else:
            best=stationary
            regime="INTERIOR_CHECKPOINT"
        payoff=max(self.net(best),0.0)
        if payoff<=0:
            raise ArithmeticError("Positive asymptotic gain must give positive attainable net benefit")
        return {"regime":regime,"optimal_wait_time":best,
                "optimal_net_value":payoff,
                "interior_stationary_point":stationary,
                "threshold_normalization":abs(self.loss_scale*self.q0-self.baseline_loss)<1e-11}


def symmetric_threshold_peak(alpha:float,beta:float)->float:
    """The special, and ONLY threshold-normalized log(1+a/b)/a formula."""
    if not isfinite(alpha) or not isfinite(beta) or alpha<=0 or beta<=0:
        raise ValueError("alpha,beta must be finite and positive")
    return log(1+alpha/beta)/alpha


def explicit_nonzero_wait_cost_stationarity(t:float,model:ActionabilityPeak,
                                            marginal_waiting_cost:float)->float:
    """Exact first-order residual N'(t) for cumulative C(t) cost.

    An interior optimum solves:
    r*S*q' + r'*(S*q-B) - C' = 0.
    Merely solving stationarity does not ensure a global optimum.
    """
    if not isfinite(marginal_waiting_cost) or marginal_waiting_cost<0:
        raise ValueError("Nonnegative finite direct waiting marginal cost required")
    return model.derivative(t)-marginal_waiting_cost


def linear_phase_expectation(
    e: float, prior_mean: float, phi: float, h: float,
    k: float, innovation_mean: float = 0.0
) -> dict:
    """Conditional phase expectation, including the nonzero prior intercept."""
    vals=(e, prior_mean, phi, h, k, innovation_mean)
    if not all(isfinite(z) for z in vals):
        raise ValueError("All phase parameters must be finite")
    if not 0 <= k <= 1 or not 0 <= h <= 1:
        raise ValueError("Cue fraction and correction fraction must lie in [0,1]")
    estimated=prior_mean+k*(e-prior_mean)
    direct=phi*(e-h*estimated)+innovation_mean
    slope=phi*(1-h*k)
    intercept=-phi*h*(1-k)*prior_mean+innovation_mean
    return {
        "direct":direct,
        "slope":slope,
        "intercept":intercept,
        "decomposed":slope*e+intercept,
        "identifies_h_and_k_separately":False,
    }


def noisy_cue_phase_variance(
    p: float, measurement_variance: float, phi: float,
    h: float, innovation_variance: float
) -> dict:
    """Linear-Gaussian variance, not incorrectly lambda^2*P.

    Prior phase P, independent observation variance R, Kalman gain
    K=P/(P+R), correction fraction h and independent process Q.
    """
    values=(p,measurement_variance,phi,h,innovation_variance)
    if not all(isfinite(z) for z in values):
        raise ValueError("Nonfinite Gaussian model parameter")
    if p<=0 or measurement_variance<0 or not 0<=h<=1 or innovation_variance<0:
        raise ValueError("P>0, R>=0, h in [0,1] and Q>=0 required")
    k=p/(p+measurement_variance)
    retention=phi*(1-h*k)
    actual=(phi**2)*p*(1-k*h*(2-h))+innovation_variance
    naive=(retention**2)*p
    extra=(phi**2)*(h**2)*k*(1-k)*p+innovation_variance
    return {
        "kalman_fraction":k,
        "conditional_mean_slope":retention,
        "actual_p_next":actual,
        "retention_squared_times_p":naive,
        "noise_and_estimation_gap":extra,
        "difference":actual-naive,
        "new_data_estimated":False,
    }


def two_actor_mismatch(
    e1_initial:float,e2_initial:float,lambda1:float,lambda2:float,steps:int
)->dict:
    """Exact no-innovation two-actor scalar retention identity."""
    if type(steps) is not int or steps<0:
        raise ValueError("nonnegative integral checkpoint count required")
    if not all(isfinite(x) for x in (e1_initial,e2_initial,lambda1,lambda2)):
        raise ValueError("finite initial phases/retentions required")
    x1=lambda1**steps *e1_initial
    x2=lambda2**steps *e2_initial
    d0=e1_initial-e2_initial
    m0=(e1_initial+e2_initial)/2
    inherited=(lambda1**steps+lambda2**steps)*d0/2
    controller=(lambda1**steps-lambda2**steps)*m0
    return {"direct":x1-x2,"inherited":inherited,
            "controller_asymmetry":controller,"decomposed":inherited+controller,
            "innovation_free":True,"ecological_fitness":None}
