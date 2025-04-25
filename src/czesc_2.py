import random


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
    skl_0 = x_c % len(tab_perm)
    return skoki_perm(tab_perm, 0, skl_0)


def funkcja_skrotu_1d_perm_v1(x_c, tab_perm):
    dtw = len(tab_perm)
    skl_0 = x_c % dtw
    skl_1 = (x_c // dtw) % dtw
    return skoki_perm(tab_perm, 0, skl_0, skl_1)


def funkcja_skrotu_1d_perm_v2(x_c, tab_perm):
    dtw = len(tab_perm)
    skl_0 = x_c % dtw
    skl_1 = (x_c // dtw) % dtw
    skl_2 = (x_c // (dtw**2)) % dtw
    return skoki_perm(tab_perm, 0, skl_0, skl_1, skl_2)


def funkcja_skrotu_1d_perm_v3(x_c, tab_perm):
    dtw = len(tab_perm)

    czy_ujemne = 0
    if x_c < 0:
        czy_ujemne = 1
        x_c = -x_c

    wynik = tab_perm[x_c % tab_perm]
    x_c = x_c // dtw
    while x_c > 0:
        wynik = tab_perm[wynik + (x_c % dtw)]
        x_c = x_c // dtw

    ???