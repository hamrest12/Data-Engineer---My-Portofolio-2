def bilangan_ganjil_genap(awal, akhir):
    ganjil = []
    genap = []

    for i in range(awal, akhir):
        if i % 2 == 0:
            genap.append(i)
        else:
            ganjil.append(i)

    return ganjil, genap

def bilangan_prima(akhir):
    prima = []
    for i in range(2, akhir):
        is_prime = True
        for j in range(2, int(i ** 0.5)+1):
            if i % j == 0:
                is_prime = False
                break
            
        if is_prime:
            prima.append(i)

    return prima

def bukan_prima(akhir):
    bkn_prima = []
    for i in range(2, akhir):
        for j in range(2, int(i ** 0.5)+1):
            if i % j == 0:
                bkn_prima.append(i)
                break
                        
    return bkn_prima

def fibonaci(jml_iterasi):
    fibonaci = []
    
    for i in range(jml_iterasi):
        if i < 2:
            fibonaci.append(i)
        else:
            fibonaci.append(fibonaci[i-2]+fibonaci[i-1])
    return fibonaci

def not_fibo():
    fibonaci = []
    not_fibonaci = []

    for i in range(5):
        is_fibonaci = False
        if i < 2:
            fibonaci.append(i)    
        else:
            fibonaci.append(fibonaci[i-2]+fibonaci[i-1])
            
            for j in range(5):
                not_fibonaci.append(j)

    return fibonaci, not_fibonaci




print(not_fibo())

# print(bilangan_ganjil_genap(1, 10))
# print(bilangan_prima(23))
# print(bukan_prima(23))
