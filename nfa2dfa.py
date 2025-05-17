import copy as c

def nfa_reform(nfa):
    ### TOBB KARAKTERES ATMENETEKET SZETSZEDI
    tmp_set = set()
    REFORM = 1
    while (REFORM):
        REFORM = 0
        for i in range(len(nfa)):
            for j in range(len(nfa[i])):
                for s in nfa[i][j]:
                    if len(s) > 1:
                        tmp_set = set()
                        s1 = s[0]
                        s2 = s[1:]
                        for t in range(len(nfa)):
                            if (t == i):
                                nfa[t].append({s1})
                            else:
                                nfa[t].append(set())
                        nfa.append(list(set() for k in range(len(nfa) + 1)))
                        nfa[-1][j].add(s2)
                        tmp_set.add(s)
                        REFORM = 1
                nfa[i][j] -= tmp_set


def main():
    ### NFA PARAMETEREI
    # 1. ORA FEALADAT
    nfa = [[set(), {'a'}, {'e'}, set()],
           [set(), {'b'}, {'b'}, {'a'}],
           [set(), {'a'}, set(), {'ab'}],
           [{'a'}, set(), set(), {'b'}]]
    sigma = ['a', 'b']
    s_nfa = 0
    f_nfa = {1, 3}


    # 2. ORAI FELADAT
    # nfa = [[{'b'}, {'a'}, {'a'}, set(), set()],
    #        [set(), {'a'}, set(), {'a', 'b'}, set()],
    #        [set(), set(), set(), {'e'}, {'a'}],
    #        [{'b'}, set(), set(), set(), {'e'}],
    #        [{'b'}, set(), set(), set(), set()]]
    # sigma = ['a', 'b']
    # s_nfa = 0
    # f_nfa = {0}


    # 3. ORAI FEALADAT
    # nfa = [[set(), {'a', 'b'}, {'a'}, set(), set()],
    #        [{'b'}, {'a'}, set(), set(), set()],
    #        [set(), {'b'}, {'b'}, {'e'}, set()],
    #        [set(), set(), set(), set(), {'ba'}],
    #        [set(), {'a', 'b'}, {'a'}, set(), set()]]
    # sigma = ['a', 'b']
    # s_nfa = 0
    # f_nfa = {2}

    nfa_reform(nfa)

    k_nfa = len(nfa)



    ### DFA PARAMETEREI
    # DFA ALLAPOTAI ATMENETEKKEL EGYUTT
    dfa = list()
    # sigma

    # ELFOGADO ALLAPOTOK
    f_dfa = set()

    # KEZDOALLAPOT MEGHATAROZASA
    s_dfa = {s_nfa}
        # e ELEK VIZSGALATA
    s_dfa_eexam_stack = list()
    s_dfa_eexam_stack.append(s_nfa)
    s_dfa_examined = set()
    while len(s_dfa_eexam_stack) > 0:
        s_dfa_exam = s_dfa_eexam_stack.pop(-1)
        s_dfa_examined.add(s_dfa_exam)
        for eEx in range(len(nfa[s_dfa_exam])):
            if ('e' in nfa[s_dfa_exam][eEx]):
                s_dfa.add(eEx)
                if eEx not in s_dfa_examined:
                    s_dfa_eexam_stack.append(eEx)


    # FELTERKEPEZENDO ALLAPOTOK VERME
    k_stack_dfa = [s_dfa]

    # KOVETKEZO VIZSGALT ALLAPOT
    while (len(k_stack_dfa) != 0):
        k_act_dfa = k_stack_dfa.pop(-1)

        tmp_list = list(range(len(sigma) + 1))
        tmp_list[0] = k_act_dfa
        for char in range(1, len(sigma) + 1):
            k_next_dfa = set()
            for k in k_act_dfa:
                for nfa_state in range(k_nfa):
                    if (sigma[char - 1] in nfa[k][nfa_state]):
                        k_next_dfa.add(nfa_state)

                        # e ELEK VIZSGALATA
                        nfa_state4e_stack = list()
                        nfa_state4e_examined = set()
                        nfa_state4e_stack.append(nfa_state)
                        while len(nfa_state4e_stack) > 0:
                            nfa_state_exam = nfa_state4e_stack.pop(-1)
                            nfa_state4e_examined.add(nfa_state_exam)
                            for eEx in range(len(nfa[nfa_state_exam])):
                                if ('e' in nfa[nfa_state_exam][eEx]):
                                    k_next_dfa.add(eEx)
                                    if eEx not in nfa_state4e_examined:
                                        nfa_state4e_stack.append(eEx)

            tmp_list[char] = k_next_dfa

            ### HA MEG A KAPOTT ALLAPOTOT NEM VIZSGALTUK ES NINCS IS BENNE A STACK-BEN,
            ### AKKOR FELVESSZUK A STACK-BE
            if (k_act_dfa != k_next_dfa):
                OK = 1
                for i in dfa:
                    if (i[0] == k_next_dfa):
                        OK = 0
                        break
                for i in k_stack_dfa:
                    if (i == k_next_dfa):
                        OK = 0
                        break
                if OK:
                    k_stack_dfa.append(k_next_dfa)

        ### KAPOTT ALLAPOT ATMENETEKKEL HOZZAADASA DFA-HOZ
        dfa.append(list(range(len(tmp_list))))
        dfa[-1] = c.copy(tmp_list)

    ### ELFOGADO ALLAPOTOK
    for i in range(len(dfa)):
        for k in dfa[i][0]:
            if k in f_nfa:
                f_dfa.add(i)
    print()


    ### ALLAPOTOK SZAMANAK INCREMENTALASA, HOGY NE 0 LEGYEN AZ ELSO ALLAPOT
    for i in range(len(dfa)):
        for k in range(len(dfa[i])):
            dfa[i][k] = set(map(lambda x: x + 1, dfa[i][k]))
    s_dfa = set(map(lambda x: x + 1, s_dfa))
    f_dfa = set(map(lambda x: x + 1, f_dfa))


    ### ALLAPOTOK HALMAZANAK KIIRATASA
    Q = dict()
    for d in range(len(dfa)):
        Q[f'Q{d + 1}'] = dfa[d][0]

    print("DFA: ")
    print("K = {", end = '')
    s = 0
    for q in Q:
        s += 1
        if s != len(Q):
            print(f"{q}", end = ', ')
        else:
            print(f"{q}", end='')
    print('}')
    print('\tahol')
    for q in Q:
        if (Q[q] != set()):
            print(f"\t{q} = {Q[q]}")
        else:
            print(f"\t{q} = \u00F8")
    print()


    ### ABECE
    print("\u03A3 =", set(sigma))
    print()


    ### HOZZARENDELESI FUGGVENY
    print('\u03B4 függvény:')
    for r in range(len(dfa)):
        for s in range(len(sigma)):
            print(f'\u03B4(Q{r + 1}, {sigma[s]}) = ', end = '')
            for h in range(len(dfa)):
                if (dfa[r][s + 1] == dfa[h][0]):
                    print(f'Q{h + 1}')
    print()


    ### KEZDO ALLAPOT
    for k in range(len(dfa)):
        if dfa[k][0] == s_dfa:
            print(f"s = Q{k + 1}")
    print()


    ### ELFOGADO ALLAPOTOK
    s = 0
    print("F = {", end='')
    for f in f_dfa:
        s += 1
        if (s != len(f_dfa)):
            print(f"Q{f}", end=', ')
        else:
            print(f"Q{f}", end='')
    print('}')


main()
