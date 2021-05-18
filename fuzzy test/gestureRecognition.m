clear all       % очистка пам€ти (leaving the workspace empty)
clc             % очистка командного окна  (Clear Command Window)

fist_I = [[60, 90, 90, 90, 90]' [0.086 0.066 0.066 0.066 0.066]'];
fist_O = 0;
palm_I = [[10 4 0 3 1]' [0.64 0.8 1 0.96 0.99]'];
palm_O = 0.102;
ok_I = [[60 45 25 15 5]' [0.086 0.12 0.24 0.455 0.96]'];
ok_O = 0.2078;
good_I = [[0 85 84 90 89]' [1 0.07 0.07 0.066 0.066]'];
good_O = 0.3073;
one_I = [[85 0 70 80 90]' [0.07 1 0.08 0.072 0.066]'];
one_O = 0.4;
c_I = [[50 40 20 17 5]' [0.1 0.14 0.27 0.3 0.96]'];
c_O = 0.5761;
d_I = [[78 0 45 40 31]' [0.072 1 0.12 0.14 0.2]']; 
d_O = 0.6609;
i_I = [[80 80 80 80 10]' [0.072 0.072 0.072 0.072 0.64]'];
i_O = 0.7733;
rock_I = [[70 10 75 80 20]' [0.08 0.64 0.077 0.072 0.27]'];
rock_O = 0.8898;
two_I = [[80 0 10 70 80]' [0.072 1 0.64 0.08 0.072]'];
two_O = 1;

I_ob = [fist_I(:, 2) palm_I(:, 2) ok_I(:, 2) good_I(:, 2) one_I(:, 2) ...
        c_I(:, 2) d_I(:, 2) i_I(:, 2) rock_I(:, 2) two_I(:, 2)];
    
O_ob = [fist_O palm_O ok_O good_O one_O c_O d_O i_O rock_O two_O]';

fis = readfis('multiVar.fis');

%  оэффициенты конццентрации термов переменных
thumb_s1 = fis.input(1).mf(1).params(1);	% 
thumb_s2 = fis.input(1).mf(2).params(1);	% 
thumb_s3 = fis.input(1).mf(3).params(1);	% 

index_s1 = fis.input(2).mf(1).params(1);	%   
index_s2 = fis.input(2).mf(2).params(1);
index_s3 = fis.input(2).mf(3).params(1);

middle_s1 = fis.input(3).mf(1).params(1);	% 
middle_s2 = fis.input(3).mf(2).params(1);	% 
middle_s3 = fis.input(3).mf(3).params(1);	% 

ring_s1 = fis.input(4).mf(1).params(1);	% 
ring_s2 = fis.input(4).mf(2).params(1);	% 
ring_s3 = fis.input(4).mf(3).params(1);	% 

little_s1 = fis.input(5).mf(1).params(1);	%
little_s2 = fis.input(5).mf(2).params(1);	%
little_s3 = fis.input(5).mf(3).params(1);	%

I_s = [thumb_s1  thumb_s2  thumb_s3 ...    % объедин.цент.конц. в один вектор
       index_s1  index_s2  index_s3 ...
       middle_s1   middle_s2   middle_s3 ...
       ring_s1  ring_s2  ring_s3 ...
       little_s1  little_s2  little_s3];
I_sL = 0.3*I_s;    % нижн€€ граница = начальное приближение - 70%                      
I_sU = 1.7*I_s;	% верхн€€ граница = начальное приближение + 70%
  

thumb_c1 = fis.input(1).mf(1).params(2);	% 
thumb_c2 = fis.input(1).mf(2).params(2);	% 
thumb_c3 = fis.input(1).mf(3).params(2);	% 

index_c1 = fis.input(2).mf(1).params(2);	%   
index_c2 = fis.input(2).mf(2).params(2);
index_c3 = fis.input(2).mf(3).params(2);

middle_c1 = fis.input(3).mf(1).params(2);	% 
middle_c2 = fis.input(3).mf(2).params(2);	% 
middle_c3 = fis.input(3).mf(3).params(2);	% 

ring_c1 = fis.input(4).mf(1).params(2);	% 
ring_c2 = fis.input(4).mf(2).params(2);	% 
ring_c3 = fis.input(4).mf(3).params(2);	% 

little_c1 = fis.input(5).mf(1).params(2);	%
little_c2 = fis.input(5).mf(2).params(2);	%
little_c3 = fis.input(5).mf(3).params(2);	%

I_c = [thumb_c1  thumb_c2  thumb_c3 ...    
       index_c1  index_c2  index_c3 ...
       middle_c1   middle_c2   middle_c3 ...
       ring_c1  ring_c2  ring_c3 ...
       little_c1  little_c2  little_c3];
   
I_cL = 0.3*I_c;    % нижн€€ граница = начальное приближение - 70%                      
I_cU = 1.7*I_c;	% верхн€€ граница = начальное приближение + 70%
  
ParamFis0 = [I_s  I_c];       % начальное приближение
ParamFisL = [I_sL  I_cL];       % нижн€€ граница
ParamFisU = [I_sU  I_cU];       % верхн€€ граница

% ћасштабир.настраив.параметров

Msht = [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1];   % отсутствие масшт.парам.
ParamFis0 = ParamFis0 .* Msht;
ParamFisL = ParamFisL .* Msht;
ParamFisU = ParamFisU .* Msht;

%---------------------------------------------
% ѕј–јћ≈“–џ ќѕ“»ћ»«ј÷»»

optimset('fmincon');     % вывод структуры с инф.о парам. алгоритма оптим.  

% options = [];
options = optimset('Display', 'iter');      % вывод инф. на каждой итерации
options.MaxIter = 25;                       % максимальное число итераций
options.DiffMinChange = 0.0001;
options.DiffMaxChange = 0.2;
options.LargeScale = 'off';
%---------------------------------------------

[ParamFis_opt, sqrtFis, flag] = fmincon(@errFisGesture, ParamFis0, [], [], [], [], ...
    ParamFisL, ParamFisU, [], options, fis, I_ob, O_ob, Msht)

fisOpt = changeFisGesture(ParamFis_opt, fis, Msht);	% сист.нечЄт.выв.после оптимиз.
%fuzzy(fisOpt);
