"""
the implementation of preprocessing method for phase denoising in
    [1]F. Meneghello, D. Garlisi, N. D. Fabbro, I. Tinnirello, and M. Rossi,
    “Environment and Person Independent Activity Recognition with a Commodity
    IEEE 802.11ac Access Point,” arXiv:2103.09924 [cs, eess], Mar. 2021,
    Accessed: Jun. 25, 2021. [Online]. Available: http://arxiv.org/abs/2103.09924
by ZX
"""
import numpy as np
import scipy.optimize


class EPIAR():
    def __init__(self, subcarriers_index,num_path=20, T=3.2e-6,lambda_parameter=0.01, Fc=5.0e9):
        """
        :param subcarriers_index: the index of the captured sub-carriers
        :param num_path: the assumption of the number of paths
        :param T: the duration of OFDM symbol, constantly 3.2e-6
        :param lambda_parameter: the optimization loss parameter
        :param Fc: the center frequency of the WiFi channel (~2.4G or ~5G)
        """
        self.num_path = num_path
        self.subcarriers_index = subcarriers_index
        self.num_subcarriers = len(subcarriers_index)
        self.T = T
        self.h = np.ones(self.num_subcarriers, dtype=np.complex)
        self.lambda_parameter = lambda_parameter
        self.Fc = Fc

    def construct_model(self,Tp,Ap,SFO,PDD,CFO,PPO,PA,):
        """
        :param Tp: the time delay of the p-th path
        :param Ap: the attenuation factor of the p-th path
        :param SFO: the sampling frequency offset
        :param PDD: the packet detection delay
        :param CFO: the channel frequency offset
        :param PPO: the phase-locked loop
        :param PA: the phase ambiguity
        :return: the estimated CSI (t_r)
        """
        assert len(Tp) == self.num_path, 'the length of Tp must be equal to the number of paths'
        assert len(Ap) == self.num_path, 'the length of Ap must be equal to the number of paths'
        t_matrix = np.ones((self.num_subcarriers,self.num_path), dtype=np.complex)
        for m in range(self.num_subcarriers):
            for p in range(self.num_path):
                t_matrix[m,p] = np.exp(-1j*2*np.pi*self.subcarriers_index[m]*(Tp[p]+SFO+PDD))

        r_vector = np.ones(self.num_path,dtype=np.complex)
        constant_phaseoffs = np.exp(1j*CFO*PPO*PA)
        for p in range(self.num_path):
            r_vector[p] = np.exp(Ap[p]*np.exp(-1j*2*np.pi*self.Fc*Tp[p]))
        r_vector *= constant_phaseoffs
        t_r = np.matmul(t_matrix,r_vector)
        return t_matrix,r_vector,t_r

    def model_loss(self,initial_parameter):
        """
        :param initial_parameter: the initial parameters for optimization
        :return: the loss between real CSI and the estimated CSI
        """
        Tp  = initial_parameter[0:self.num_path]
        Ap  = initial_parameter[self.num_path:2*self.num_path]
        SFO = initial_parameter[2*self.num_path]
        PDD = initial_parameter[2*self.num_path+1]
        CFO = initial_parameter[2*self.num_path+2]
        PPO = initial_parameter[2*self.num_path+3]
        PA  = initial_parameter[2*self.num_path+4]
        t_matrix, r_vector, t_r = self.construct_model(Tp,Ap,SFO,PDD,CFO,PPO,PA,)
        loss = np.linalg.norm(self.h - t_r) + self.lambda_parameter * np.linalg.norm(r_vector, ord=1)
        return loss

    def find_optimal(self,h, initial_parameter):
        """
        :param h: the real CSI vector
        :param initial_parameter: the initial parameter of CSI model
        :return: the optimal estimated model
        """
        self.h = h
        optimal_parameters = scipy.optimize.fmin_bfgs(self.model_loss,initial_parameter)
        Tp = optimal_parameters[0:self.num_path]
        Ap = optimal_parameters[self.num_path:2 * self.num_path]
        SFO = optimal_parameters[2 * self.num_path]
        PDD = optimal_parameters[2 * self.num_path + 1]
        CFO = optimal_parameters[2 * self.num_path + 2]
        PPO = optimal_parameters[2 * self.num_path + 3]
        PA = optimal_parameters[2 * self.num_path + 4]
        t_matrix_optimal, r_vector_optimal, t_r_optimal = self.construct_model(Tp, Ap, SFO, PDD, CFO, PPO, PA, )
        return t_matrix_optimal, r_vector_optimal, t_r_optimal

    def denoise(self,h, initial_parameter):
        """
        :param h: the real CSI vector
        :param initial_parameter: the initial parameter of CSI model
        :return: the denoised CSI
        """
        t_matrix_optimal, r_vector_optimal, t_r_optimal = test.find_optimal(h, initial_parameter)
        X = np.ones((self.num_subcarriers,self.num_path), dtype=np.complex)
        for m in range(self.num_subcarriers):
            X[m,:] = r_vector_optimal*t_matrix_optimal[m,:]

        max_amp_path = np.argmax(r_vector_optimal)
        for m in range(self.num_subcarriers):
            X[m, :] = np.conj(t_matrix_optimal[m, max_amp_path]) * t_matrix_optimal[m, :]
        return np.sum(X,axis=1)


if __name__ == "__main__":
    # subcarriers_index_part1 = [i for i in range(-122,-1)]
    # subcarriers_index_part2 = [i for i in range(2,123)]
    # subcarriers_index = subcarriers_index_part1 + subcarriers_index_part2

    subcarriers_index = [-2,-1,1,]
    test = EPIAR(subcarriers_index,num_path=4)
    Tp = [1e-4,3e-3,2e-4,1e-5]
    Ap = [0.25,0.5,0.63,0.1]
    other = [1e-4,3e-3,2e-4,1e-4,2e-4,]
    initial = Tp+Ap+other
    h = [5.91552818+5.37260757e-09j, 5.91344323-1.49513892e-01j,5.90719052-2.98899580e-01j]
    result = test.denoise(h,initial)
    print(h)
    print(result)