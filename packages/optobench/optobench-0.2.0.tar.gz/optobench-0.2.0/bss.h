#ifndef _BSS_H
#define _BSS_H

#include <vector>

double ackley(const std::vector<double>& xs);
double alpine(const std::vector<double>& xs);
double bohachevsky1(const std::vector<double>& xs);
double bohachevsky2(const std::vector<double>& xs);
double bohachevsky3(const std::vector<double>& xs);
double bukin_f6(const std::vector<double>& xs);
double cross_in_tray(const std::vector<double>& xs);
double eggholder(const std::vector<double>& xs);
double gramacy_lee(const std::vector<double>& xs);
double holder_table(const std::vector<double>& xs);
double langermann(const std::vector<double>& xs);
double levy(const std::vector<double>& xs);
double levy13(const std::vector<double>& xs);
double six_hump_camel_back(const std::vector<double>& xs);
double dejong5(const std::vector<double>& xs);
double deceptive3(const std::vector<double>& xs);
double drop_wave(const std::vector<double>& xs);
double easom(const std::vector<double>& xs);
double penalty1(const std::vector<double>& xs);
double michalewicz(const std::vector<double>& xs);
double perm0db(const std::vector<double>& xs);
double permdb(const std::vector<double>& xs);
double non_cont_rastrigin(const std::vector<double>& xs);
double rastrigin(const std::vector<double>& xs);
double rosenbrock(const std::vector<double>& xs);
double griewank(const std::vector<double>& xs);
double goldstein_price(const std::vector<double>& xs);
double axis_parallel_hyperellipsoid(const std::vector<double>& xs);
double rotated_hyperellipsoid(const std::vector<double>& xs);
double sum_powers(const std::vector<double>& xs);
double trid(const std::vector<double>& xs);
double step(const std::vector<double>& xs);
double schaffers_f2(const std::vector<double>& xs);
double schaffers_f4(const std::vector<double>& xs);
double schaffers_f6(const std::vector<double>& xs);
double schwefels(const std::vector<double>& xs);
double schwefels_p222(const std::vector<double>& xs);
double shubert(const std::vector<double>& xs);
double sphere(const std::vector<double>& xs);
double tripod(const std::vector<double>& xs);
double trefethen4(const std::vector<double>& xs);
double three_hump_camel_back(const std::vector<double>& xs);
double dixon_price(const std::vector<double>& xs);
double beale(const std::vector<double>& xs);
double branin(const std::vector<double>& xs);
double colville(const std::vector<double>& xs);
double styblinski_tang(const std::vector<double>& xs);
double powell(const std::vector<double>& xs);
double shekel(const std::vector<double>& xs);
double forrester(const std::vector<double>& xs);
double hartmann_3d(const std::vector<double>& xs);
double hartmann_4d(const std::vector<double>& xs);
double hartmann_6d(const std::vector<double>& xs);
double booth(const std::vector<double>& xs);
double matyas(const std::vector<double>& xs);
double mccormick(const std::vector<double>& xs);
double power_sum(const std::vector<double>& xs);
double zakharov(const std::vector<double>& xs);

#endif // _BSS_H

