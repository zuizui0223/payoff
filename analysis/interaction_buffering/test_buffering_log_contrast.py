import pytest
np = pytest.importorskip('numpy')
from buffering_log_contrast import (log_mean_contrasts, independent_mean_covariance,
                                     factorial_buffer)


def test_factorial_attenuation():
    m = [10, 5, 10, 8]
    v = independent_mean_covariance([2]*4,[10]*4, independent_arms_verified=True)
    out = factorial_buffer(m,v)
    assert out['theta'] == pytest.approx(np.log(1.6))
    assert out['low_buffer_detrimental_point_estimate']
    assert out['covariance'][2][2] == pytest.approx(sum(np.diag(v)/np.array(m)**2))


def test_shared_control_covariance():
    m = [10,7,4]
    v = np.diag([.5,.6,.7])
    est, cv = log_mean_contrasts(m,v,[[-1,1,0],[-1,0,1]])
    assert est.tolist() == pytest.approx([np.log(.7),np.log(.4)])
    assert cv[0,1] == pytest.approx(.005)


def test_paired_arms_covariance():
    m = [10,5,10,8]
    v = np.eye(4)*.5 + np.ones((4,4))*.1
    out = factorial_buffer(m,v)
    g = np.array([1,-1,-1,1])/m
    assert out['covariance'][2][2] == pytest.approx(g@v@g)


@pytest.mark.parametrize('m,v,c', [([0,2],np.eye(2),[-1,1]),
    ([1,2],[[1,2],[2,1]],[-1,1]), ([1,2],[[1,0],[.1,1]],[-1,1]),
    ([1,2],np.eye(2),[0,1]), ([1,2],np.eye(3),[-1,1])])
def test_invalid_inputs(m,v,c):
    with pytest.raises(ValueError): log_mean_contrasts(m,v,c)


def test_no_assumed_independence():
    with pytest.raises(ValueError): independent_mean_covariance([2]*4,[10]*4,independent_arms_verified=False)


def test_positive_delay_is_not_rescue():
    assert not factorial_buffer([10,12,10,15],np.eye(4))['low_buffer_detrimental_point_estimate']
