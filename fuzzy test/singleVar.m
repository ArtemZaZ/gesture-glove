clear all       % очистка пам€ти (leaving the workspace empty)
clc             % очистка командного окна  (Clear Command Window) 

n = 10;         % количество точек дискретизации
angle_real = linspace(0, 90, n);
dR_Rm_real = [1 0.64 0.27 0.2 0.14 0.1 0.086 0.08 0.072 0.066];

fis = readfis('approximator.fis');     % загрузка исходной нечЄткой сист. с диска                   

angle_appr = evalfis(dR_Rm_real, fis);

%--------------------------------------------------------------------------
% ѕроцесс адаптации системы нечЄткого вывода
%---------------------------------------------
% Ќј—“–ј»¬ј≈ћџ≈ ѕј–јћ≈“–џ (10 шт):
%    - коэф. конц.термов переменных x;
%    - коорд.максимумв термов переменных x;
%-----------------

%  оэффициенты конццентрации термов переменных
x_s10 = fis.input(1).mf(1).params(1);	% 
x_s20 = fis.input(1).mf(2).params(1);	%       -//-        	
x_s30 = fis.input(1).mf(3).params(1);	%       -//-        	
x_s40 = fis.input(1).mf(4).params(1);	%       -//- 
x_s50 = fis.input(1).mf(5).params(1);	%       -//- 

x_s0 = [x_s10 x_s20 x_s30 x_s40 x_s50];
x_s0L = 0.3*x_s0;    % нижн€€ граница = начальное приближение - 30%                      
x_s0U = 1.3*x_s0;	% верхн€€ граница = начальное приближение + 30%

x_c10 = fis.input(1).mf(1).params(2);	% исх. знач. дл€ x
x_c20 = fis.input(1).mf(2).params(2);	%       -//-        	
x_c30 = fis.input(1).mf(3).params(2);	%       -//-        	
x_c40 = fis.input(1).mf(4).params(2);	%       -//- 
x_c50 = fis.input(1).mf(5).params(2);	%       -//-

x_c0 = [x_c10  x_c20  x_c30 x_c40 x_c50];
dR = 0.3*(max(dR_Rm_real)-min(dR_Rm_real));
x_c0L = x_c0 - [dR dR dR dR dR];       % нижн€€ граница                      
x_c0U = x_c0 + [dR dR dR dR dR];       % верхн€€ граница

% ќбъединение настраиваемых параметров в один вектор 
ParamFis0 = [x_s0  x_c0];       % начальное приближение
ParamFisL = [x_s0L  x_c0L];       % нижн€€ граница
ParamFisU = [x_s0U  x_c0U];       % верхн€€ граница

% ћасштабир.настраив.параметров (демасштаб. в функц. F_changeFISmg)
% Msht = [];
Msht = [1 1 1 1 1 1 1 1 1 1];   % отсутствие масшт.парам.
ParamFis0 = ParamFis0 .* Msht;
ParamFisL = ParamFisL .* Msht;
ParamFisU = ParamFisU .* Msht;
% ѕј–јћ≈“–џ ќѕ“»ћ»«ј÷»»

optimset('fmincon')     % вывод структуры с инф.о парам. алгоритма оптим.  

% options = [];
options = optimset('Display', 'iter');      % вывод инф. на каждой итерации
options.MaxIter = 30;                       % максимальное число итераций
options.DiffMinChange = 0.0001;
options.DiffMaxChange = 0.2;
options.LargeScale = 'off';

%---------------------------------------------
% ќѕ“»ћ»«ј÷»я

[ParamFis_opt, sqrtFis, flag] = fmincon(@errFIS, ParamFis0, [], [], [], [], ...
    ParamFisL, ParamFisU, [], options, fis, dR_Rm_real, angle_real', Msht);

fisOpt = changeFIS(ParamFis_opt, fis, Msht);	% сист.нечЄт.выв.после оптимиз.

% showfis(fisMgOpt)

%---------------------------------------------

angle_opt = evalfis(dR_Rm_real, fisOpt);

h1 = figure(1);          
colormap('white') 
hold on;
plot(dR_Rm_real, angle_real, 'LineWidth', 2);
plot(dR_Rm_real, angle_appr, 'LineWidth', 2);
plot(dR_Rm_real, angle_opt, 'LineWidth', 2);
legend("–еальна€ зависимость", "–учное приближение", "ќптимизаци€");
hold off
xlabel('\Delta{R/R_m}');   ylabel('\alpha, град.');
title('–езультат аппроксимации зависимости')  

% fuzzy(fisOpt)
