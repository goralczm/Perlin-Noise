from czesc_1 import *

seed = 42


def permutacja_o_dlugosci(dtw, seed):
    random.seed(seed)
    tab = list(range(dtw))
    for i in range(dtw):
        los = random.randint(0, dtw - 1)
        tmp = tab[los]
        tab[los] = tab[i]
        tab[i] = tmp

    return tab


def permutacje_podw_wygeneruj_v0(dtw, seed):
    return permutacja_o_dlugosci(dtw, seed) + permutacja_o_dlugosci(dtw, seed + 1)


def permutacje_podw_wygeneruj_v1(dtw, seed):
    return permutacja_o_dlugosci(dtw, seed) * 2


def skoki_perm(tab_perm, wynik_pocz, *skl_n):
    wynik = wynik_pocz
    for skl in skl_n:
        wynik = tab_perm[wynik + skl]

    return wynik


def funkcja_skrotu_1d_perm_v0(x_c, tab_perm):
    dtw = len(tab_perm) // 2
    skl_0 = x_c % dtw
    return skoki_perm(tab_perm, 0, skl_0)


def funkcja_skrotu_1d_perm_v1(x_c, tab_perm):
    dtw = len(tab_perm) // 2
    skl_0 = x_c % dtw
    skl_1 = (x_c // dtw) % dtw
    return skoki_perm(tab_perm, 0, skl_0, skl_1)


def funkcja_skrotu_1d_perm_v2(x_c, tab_perm):
    dtw = len(tab_perm) // 2
    skl_0 = x_c % dtw
    skl_1 = (x_c // dtw) % dtw
    skl_2 = (x_c // (dtw**2)) % dtw
    return skoki_perm(tab_perm, 0, skl_0, skl_1, skl_2)


def funkcja_skrotu_1d_perm_v3(x_c, tab_perm):
    dtw = len(tab_perm) // 2

    czy_ujemne = 0
    if x_c < 0:
        czy_ujemne = 1
        x_c = -x_c

    wynik = tab_perm[x_c % len(tab_perm)]
    x_c = x_c // dtw
    while x_c > 0:
        wynik = tab_perm[wynik + (x_c % dtw)]
        x_c = x_c // dtw

    if czy_ujemne:
        return tab_perm[wynik]

    return wynik

def interpolacja_1d_cala_vperm_nlin(x, tab_wart, tab_perm):
    x_l = math.floor(x)
    x_p = x_l + 1
    i_x_l = funkcja_skrotu_1d_perm_v3(x_l, tab_perm)
    i_x_p = funkcja_skrotu_1d_perm_v3(x_p, tab_perm)
    w_l = tab_wart[i_x_l]
    w_p = tab_wart[i_x_p]
    delta_x = x - x_l
    return interpolacja_1d_rdzen_vnlin(w_l, w_p, delta_x, vwmian)

def szum_1d_pseudoperlin_vperm3(x, tab_wart, tab_perm):
    return interpolacja_1d_cala_vperm_nlin(x, tab_wart, tab_perm)

def szum_1d_pseudoperlin_oktawy(x, tab_wart, tab_perm, oktawa_liczba, oktawa_mnoznik, oktawa_zageszczenie):
    ampl_suma = 0
    wynik = 0

    for oktawa in range(oktawa_liczba):
        wys_mnoznik = oktawa_mnoznik ** oktawa
        zageszczenie_mnoznik = oktawa_zageszczenie ** oktawa
        ampl_suma += wys_mnoznik
        wynik += wys_mnoznik * szum_1d_pseudoperlin_vperm3(x * zageszczenie_mnoznik, tab_wart, tab_perm)

    return wynik / ampl_suma

if __name__ == '__main__':
    def test_funkcja_skrotu_1d_perm_v3():
        tab_wart = [0.0000, 1.0000, 0.0244, 0.6910, 0.3388]
        tab_perm = [2, 0, 4, 1, 3, 2, 0, 4, 1, 3]

        x = np.arange(-100, 100, 1)
        y = [funkcja_skrotu_1d_perm_v3(delta, tab_perm) for delta in x]
        plt.bar(x, y)
        plt.show()

    #test_funkcja_skrotu_1d_perm_v3()

    def test_zastosowanie_funkcji_skrotu_1d_v0():
        tab_wart = [0.0000, 1.0000, 0.0244, 0.6910, 0.3388]
        tab_perm = [2, 0, 4, 1, 3, 2, 0, 4, 1, 3]

        x = np.arange(-1, 11, 1)
        y_idx = [funkcja_skrotu_1d_perm_v3(delta, tab_perm) for delta in x]
        y = [tab_wart[idx] for idx in y_idx]

        plt.bar(x, y)
        plt.show()

    #test_zastosowanie_funkcji_skrotu_1d_v0()

    def test_zastosowanie_funkcji_skrotu_1d_v1():
        tab_wart = [0.0000, 1.0000, 0.0244, 0.6910, 0.3388]
        tab_perm = [2, 0, 4, 1, 3, 2, 0, 4, 1, 3]

        x = np.arange(-1, 11, .05)
        y_idx = [funkcja_skrotu_1d_perm_v3(delta, tab_perm) for delta in range(-1, 11)]
        y = [tab_wart[idx] for idx in y_idx]
        y_interpolowane = [interpolacja_1d_cala_vnlin(wart, y) for wart in x]

        plt.plot(x, y_interpolowane)
        plt.show()

    #test_zastosowanie_funkcji_skrotu_1d_v1()

    def test_interpolacja_1d_cala_vperm_nlin():
        tab_wart = [0.0000, 1.0000, 0.0244, 0.6910, 0.3388]
        tab_perm = [2, 0, 4, 1, 3, 2, 0, 4, 1, 3]

        x = np.arange(-1, 11, .05)
        y = [interpolacja_1d_cala_vperm_nlin(delta_x, tab_wart, tab_perm) for delta_x in x]

        plt.plot(x, y)
        plt.show()

    #test_interpolacja_1d_cala_vperm_nlin()

    def test_szum_1d_pseudoperlin_vperm3():
        tab_wart = [0.0000, 1.0000, 0.0244, 0.6910, 0.3388]
        tab_perm = [2, 3, 0, 4, 1, 2, 3, 0, 4, 1]

        x = np.arange(-10, 17, .05)
        y = [szum_1d_pseudoperlin_vperm3(delta_x, tab_wart, tab_perm) for delta_x in x]

        plt.plot(x, y)
        plt.show()

    #test_szum_1d_pseudoperlin_vperm3()

    def test_losowy_szum_1d_pseudoperlina_vperm3():
        dtw = 12
        losowy_seed = random.randint(-10000, 10000)
        tab_wart = wartosci_losowe_wygeneruj_v1(dtw, losowy_seed)
        tab_perm = permutacje_podw_wygeneruj_v1(dtw, losowy_seed)

        x = np.arange(0, 51, .05)
        y = [interpolacja_1d_cala_vperm_nlin(delta_x, tab_wart, tab_perm) for delta_x in x]

        plt.plot(x, y)
        plt.title(f'Seed: {losowy_seed}')
        plt.show()

    #test_losowy_szum_1d_pseudoperlina_vperm3()

    def test_szum_1d_pseudoperlin_oktawy(oktway_liczba):
        tab_wart = [0.0000, 1.0000, 0.0244, 0.6910, 0.3388]
        tab_perm = [2, 3, 0, 4, 1, 2, 3, 0, 4, 1]

        x = np.arange(-1, 11, .01)
        y = [szum_1d_pseudoperlin_oktawy(delta_x, tab_wart, tab_perm, oktway_liczba, .5, 2) for delta_x in x]

        plt.plot(x, y)
        plt.show()

    #test_szum_1d_pseudoperlin_oktawy(1)
    #test_szum_1d_pseudoperlin_oktawy(3)
    #test_szum_1d_pseudoperlin_oktawy(6)

    def test_mala_ilosc_wartosci():
        tab_wart = [0, .5, 1]
        tab_perm = [1, 2, 0, 1, 2, 0]

        x = np.arange(-5, 6, .01)
        y = [szum_1d_pseudoperlin_oktawy(delta_x, tab_wart, tab_perm, 6, .5, 2) for delta_x in x]

        plt.plot(x, y)
        plt.show()

    #test_mala_ilosc_wartosci()

    # <--- Ćwiczenia --->
    def zadanie_1():
        testowy_seed = 0
        tab_perm = permutacje_podw_wygeneruj_v1(4, testowy_seed)
        while tab_perm != [0, 1, 2, 3, 0, 1, 2, 3]:
            testowy_seed += 1
            tab_perm = permutacje_podw_wygeneruj_v1(4, testowy_seed)

        print(f'Seed: {testowy_seed}')
        print(tab_perm)

    zadanie_1()

    def zadanie_2():
        print(f'skoki_perm([2, 0, 4, 1, 3, 2, 0, 4, 1, 3], 3, 0, 1) powinno zwrocic 4 i zwraca: {skoki_perm([2, 0, 4, 1, 3, 2, 0, 4, 1, 3], 3, 0, 1)}')
        print(f'skoki_perm([2, 0, 4, 1, 3, 2, 0, 4, 1, 3], 3, 1, 0) powinno zwrocic 1 i zwraca: {skoki_perm([2, 0, 4, 1, 3, 2, 0, 4, 1, 3], 3, 1, 0)}')
        print(f'skoki_perm([2, 0, 4, 1, 3, 2, 0, 4, 1, 3], 3, 1, 0, 1, 2) powinno zwrocic 0 i zwraca: {skoki_perm([2, 0, 4, 1, 3, 2, 0, 4, 1, 3], 3, 1, 0, 1, 2)}')

    zadanie_2()

    def zadanie_3():
        tab_perm = [1, 2, 0, 1, 2, 0]
        tab_x = [0, .7, 1]

        x = np.arange(-5, 6, 1)
        y_idx = [funkcja_skrotu_1d_perm_v3(delta_x, tab_perm) for delta_x in x]
        y = [tab_x[idx] for idx in y_idx]

        print(f'x     = {[int(delta_x) for delta_x in x]}')
        print(f'wynik = {y_idx}')

        plt.bar(x, y)
        plt.title('3. indexy z funkcji_skrotu_1d_perm_v3 w tab_x')
        plt.show()

    #zadanie_3()

    def zadanie_4():
        tab_perm = [1, 2, 0, 1, 2, 0]
        tab_x = [0, .7, 1]

        x = np.arange(-10, 11, .01)
        y = [szum_1d_pseudoperlin_oktawy(delta_x, tab_x, tab_perm, 6, .5, 2) for delta_x in x]

        plt.plot(x, y)
        plt.title('4. szum_1d_pseudoperlin_oktawy')
        plt.show()

    #zadanie_4()

    def zadanie_5():
        dtw = 4
        losowy_seed = 18
        tab_wart = wartosci_losowe_wygeneruj_v1(dtw, losowy_seed)
        tab_perm = permutacje_podw_wygeneruj_v1(dtw, losowy_seed)

        x = np.arange(-10, 21, .02)
        y = [szum_1d_pseudoperlin_oktawy(delta_x, tab_wart, tab_perm, 6, .5, 2) for delta_x in x]

        fig, axs = plt.subplots(2)
        fig.suptitle(f'5. szum_1d_pseudoperlin_oktawy ładny')
        axs[0].plot(x, y)
        axs[0].set_title('oktawy=6, mnoznik=.5, zageszczenie=2')

        y = [szum_1d_pseudoperlin_oktawy(delta_x, tab_wart, tab_perm, 6, .4, 2.3) for delta_x in x]
        axs[1].plot(x, y)
        axs[1].set_title('oktawy=6, mnoznik=.4, zageszczenie=3')
        plt.show()

    zadanie_5()
