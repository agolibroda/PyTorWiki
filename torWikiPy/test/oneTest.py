

#!/usr/bin/env python3
# -*- coding: utf-8 -*-




# ну вот, сначала надо создать массив.

// для сей:

int arrayDim = 3;
int ii, 
    jj, 
    maxPrimeNumber=0, maxIiCoord=0, maxJjCord=0,
    nameAray[arrayDim][arrayDim] ;


// проверить, что данное число есть простое
int isPrime(int curentNumber) {
    
    for (int ii=1; ii<curentNumber-1; ii++){
        curentNumber/ii (curentNumber = 8;  ii= 2; curentNumber/ii = 4 !!!!!! ) - вот тут можно пректатить цикл!!!!
                            return 0
                        (curentNumber = 7;  ii= 2; curentNumber/ii = 3.5 ++++ ) - нао взять новое значение ii и проверять!
                          
        - или целое число или дробное - значит, нам нужен остаток от деления, если остаток == 0, то число не простое..
       }
    return 1;
    }

# потом цикл для заполнения массива пользователем

 <<'вот тут нужно правильное приглашение пользователя к вводу чисел'
for (ii=0; ii<arrayDim; ii++){
    // и во тут надо сделать цикл для заполнения массива значениями!!!!
    <<'введите число '+ ii;
    nameAray[ii]<<
    }

    for (ii=0; ii<arrayDim; ii++){
        for (jj=0; jj<arrayDim; jj++){
            // и во тут надо сделать цикл для заполнения массива значениями!!!!
            out <<'введите число '+ ii ;
            cin >> nameAray[ii][jj] - // вот тут с ЄТОЙ ячейкой можно что - то сделать!!!!
           }
       }
 
# потом цикл вьівода значений массива на єкран

# потом обработка массива тем методом, которьім хочеш

    for (ii=0; ii<arrayDim; ii++){
        for (jj=0; jj<arrayDim; jj++){
            if (isPrime(nameAray[ii][jj]) ) {
                // да, єто число простое!!!!!
                        if (maxPrimeNumber < nameAray[ii][jj]) {
                            maxPrimeNumber = nameAray[ii][jj]; //!!!!!!
                            maxIiCoord = ii;
                            maxJjCord = jj;
                            }
                }
           } // 
       } //

///????????






