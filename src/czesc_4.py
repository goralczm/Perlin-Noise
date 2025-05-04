from src.czesc_3 import *

def interpolacja_1d_rdzen_PerlinaPlus(grad_l, grad_p, w_l, w_p, delta_x):
    fade = 6 * math.pow(delta_x, 5) - 15 * math.pow(delta_x, 4) + 10 * math.pow(delta_x, 3)
    return (w_l + delta_x * grad_l) * (1 - fade) + (w_p + (delta_x - 1) * grad_p) * fade

def interpolacja_1d_rdzen_Perlina(grad_l, grad_p, delta_x):
    fade = 6 * math.pow(delta_x, 5) - 15 * math.pow(delta_x, 4) + 10 * math.pow(delta_x, 3)
    return (delta_x * grad_l) * (1 - fade) + ((delta_x - 1) * grad_p) * fade

def szum_1d_PerlinaPlus_vperm3(x, tab_grad, tab_perm_grad, tab_wys, tab_perm_wys):
    x_l = math.floor(x)
    x_p = x_l + 1
    delta_x = x - x_l
    i_wys_l = funkcja_skrotu_uniw_perm_v3([x_l], tab_perm_wys)
    i_wys_p = funkcja_skrotu_uniw_perm_v3([x_p], tab_perm_wys)
    wys_l = tab_wys[i_wys_l]
    wys_p = tab_wys[i_wys_p]
    i_grad_l = funkcja_skrotu_uniw_perm_v3([x_l], tab_perm_grad)
    i_grad_p = funkcja_skrotu_uniw_perm_v3([x_p], tab_perm_grad)
    grad_l = tab_grad[i_grad_l]
    grad_p = tab_grad[i_grad_p]
    return interpolacja_1d_rdzen_PerlinaPlus(grad_l, grad_p, wys_l, wys_p, delta_x)

def szum_1d_Perlina_vperm3(x, tab_grad, tab_perm_grad):
    x_l = math.floor(x)
    x_p = x_l + 1
    delta_x = x - x_l
    i_grad_l = funkcja_skrotu_uniw_perm_v3([x_l], tab_perm_grad)
    i_grad_p = funkcja_skrotu_uniw_perm_v3([x_p], tab_perm_grad)
    grad_l = tab_grad[i_grad_l]
    grad_p = tab_grad[i_grad_p]
    return interpolacja_1d_rdzen_Perlina(grad_l, grad_p, delta_x)

def szum_1d_PerlinaPlus_oktawy(x, tab_grad, tab_perm_grad, tab_wys, tab_perm_wys, oktawa_liczba, oktawa_mnoznik, oktawa_zageszczenie, oktawa_czy_zmnn_ampl):
    ampl_suma = 0
    wy = 0
    for okt_n in range(oktawa_liczba):
        mnoznik_wy_akt = math.pow(oktawa_mnoznik, okt_n)
        mnoznik_x_akt = math.pow(oktawa_zageszczenie, okt_n)
        ampl_suma += mnoznik_wy_akt
        wy += mnoznik_wy_akt * szum_1d_PerlinaPlus_vperm3(x * mnoznik_x_akt, tab_grad, tab_perm_grad, tab_wys, tab_perm_wys)

    if oktawa_czy_zmnn_ampl:
        wy /= ampl_suma

    return wy

if __name__ == "__main__":
    def test_inerpolacja_1d_rdzen_Perlina_PerlinaPlus():
        dtw = 5
        tab_wys = [0, 0.25, .5, .75, 1]
        tab_perm_wys = [2, 0, 4, 1, 3, 2, 0, 4, 1, 3]
        dtg = 4
        tab_grad = [-1, -0.33, 0.33, 1]
        tab_perm_grad = [3, 2, 0, 1, 3, 2, 0, 1]

        x = np.arange(-1, 3, .05)
        y_pseudo_perlin = [szum_1d_pseudoperlin_vperm3(delta_x, tab_wys, tab_perm_wys) for delta_x in x]
        y_perlin_plus = [szum_1d_PerlinaPlus_vperm3(delta_x, tab_grad, tab_perm_grad, tab_wys, tab_perm_wys) for delta_x in x]
        y_perlin = [szum_1d_Perlina_vperm3(delta_x, tab_grad, tab_perm_grad) for delta_x in x]

        fig, ax = plt.subplots()

        l1, = ax.plot(x, y_perlin_plus)
        l2, = ax.plot(x, y_pseudo_perlin)
        l3, = ax.plot(x, y_perlin)

        ax.legend((l1, l2, l3), ('szum Perlina+', 'szum Pseudo Perlina', 'szum Perlina'))
        plt.show()

    #test_inerpolacja_1d_rdzen_Perlina_PerlinaPlus()

    def test_szum_1d_PerlinaPlus_oktawy():
        dtw = 5
        tab_wys = [0.0000, 0.2500, .5000, .7500, 1.0000]
        tab_perm_wys = [2, 0, 4, 1, 3, 2, 0, 4, 1, 3]
        dtg = 4
        tab_grad = [-1.0000, -0.3333, 0.3333, 1.0000]
        tab_perm_grad = [3, 2, 0, 1, 3, 2, 0, 1]
        oktawa_mnoznik = .5
        oktawa_zageszczenie = 2
        oktawa_czy_zmn_ampl = True

        x = np.arange(-1, 3, .01)
        y_perlin_plus = [szum_1d_PerlinaPlus_oktawy(delta_x, tab_grad, tab_perm_grad, tab_wys, tab_perm_wys, 1, oktawa_mnoznik, oktawa_zageszczenie, oktawa_czy_zmn_ampl) for delta_x in x]
        y_perlin_plus_oktaw_2 = [szum_1d_PerlinaPlus_oktawy(delta_x, tab_grad, tab_perm_grad, tab_wys, tab_perm_wys, 2, oktawa_mnoznik, oktawa_zageszczenie, oktawa_czy_zmn_ampl) for delta_x in x]
        y_perlin_plus_oktaw_4 = [szum_1d_PerlinaPlus_oktawy(delta_x, tab_grad, tab_perm_grad, tab_wys, tab_perm_wys, 4, oktawa_mnoznik, oktawa_zageszczenie, oktawa_czy_zmn_ampl) for delta_x in x]

        fig, ax = plt.subplots()

        l1, = ax.plot(x, y_perlin_plus)
        l2, = ax.plot(x, y_perlin_plus_oktaw_2)
        l3, = ax.plot(x, y_perlin_plus_oktaw_4)

        ax.legend((l1, l2, l3), ('szum org.', '#oktaw=2', '#oktaw=4'))
        plt.show()

    #test_szum_1d_PerlinaPlus_oktawy()

    # <--- Ćwiczenia ---->
    def zadanie_2():
        test_inerpolacja_1d_rdzen_Perlina_PerlinaPlus()

    zadanie_2()

    def zadanie_3():
        test_szum_1d_PerlinaPlus_oktawy()

    zadanie_3()