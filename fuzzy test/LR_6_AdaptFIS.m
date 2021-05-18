%   Нечёткая аппроксимация зависимости: y=x1^2-x2^2
%                                                         (LR_6_AdaptFIS.m)
%
%  <<<        Адаптация системы нечёткого вывода Мамдани       >>>
%  <<< с использованием функции нелинейной оптимизации fmincon >>>
%  <<<              пакета Optimization Toolbox                >>>
%==========================================================================
clear all       % очистка памяти (leaving the workspace empty)
clc             % очистка командного окна  (Clear Command Window)  
%--------------------------------------------------------------------------
% Построение графика функции  y=x1^2-x2^2
% в области    x1 = [-6, 6];  x2 = [-6, 6]
%---------------------------------------------

n = 15;         % количество точек дискретизации
x1 = linspace(-6, 6, n);
x2 = linspace(-6, 6, n);

y = zeros(n, n);
for i = 1:n
    y(i,:) = x1.^2 - x2(i).^2;    
end    

%---------------------------------------------
h1 = figure(1);
set(h1,'Position',[5 350 520 410])
surf(x1, x2, y)
axis([-6     6 ...
      -6	6 ...
      -40   40]); 
view(-40,30)
xlabel('x_1');   ylabel('x_2');   zlabel('y');
title('Исходная зависимость')  

%--------------------------------------------------------------------------
% Построение графика нечёткого отображения Мамдани
% с гауссовыми функциями принадл. термов вх.перем.
%---------------------------------------------

fisMg = readfis('firstMg2.fis');     % загрузка исходной нечёткой сист. с диска
% fuzzy(fisMg)                    % вызов FIS-Editor с исходной неч.сист.

yMg = zeros(n, n);
for i = 1:n
    yMg(i,:) = evalfis([x1; ones(size(x1))*x2(i)], fisMg)';    
end  

%---------------------------------------------

h2 = figure(2);
set(h2,'Position',[5 -150 520 410])
colormap('default')
surf(x1, x2, yMg)
axis([-6     6 ...
      -6	6 ...
      -40   40]); 
view(-40,30)
xlabel('x_1');   ylabel('x_2');   zlabel('y');
title('Система нечёткого вывода Мамдани до адаптации') 

%--------------------------------------------------------------------------
% Формирование обучающего и тестового массивов данных
%---------------------------------------------

Nob = 60;                       % количество точек обучающего массива 
Nts = 60;                       % количество точек тестового массива 

RndStt = 3;                     %  уст.начальн.сост.генер.случ.чисел
rand('state', RndStt);

% Входы:
x1ob = min(x1)+(max(x1)-min(x1))*rand(Nob,1);
x2ob = min(x2)+(max(x2)-min(x2))*rand(Nob,1);
x1ts = min(x1)+(max(x1)-min(x1))*rand(Nts,1);
x2ts = min(x2)+(max(x2)-min(x2))*rand(Nts,1);

% Выходы:

yob = zeros(size(x1ob));
for i = 1:Nob
    yob(i) = x1ob(i)^2 - x2ob(i)^2;    
end   

yts = zeros(size(x1ts));
for i = 1:Nts
    yts(i) = x1ts(i)^2 - x2ts(i)^2;
end

%---------------------------------------------

h3 = figure(3);
set(h3,'Position',[540    -150   520   410]);
clf
hold on
plot(x1ob, x2ob, 'bs', 'MarkerSize',4)
plot(x1ts, x2ts, 'ro', 'MarkerSize',4)
hold off
axis([min(x1)-0.01  max(x1)+0.01 ...
      min(x2)-0.01  max(x2)+0.01]); 
xlabel('x1');   ylabel('x2');
title('Распределение данных обучающей (bs) и тестовой (or) выборок') 

%---------------------------------------------

pause(2);               % пауза 2,0 с

figure(2);          
colormap('white')     % 
hold on
plot3(x1ob, x2ob, yob, 'bs', 'MarkerSize',3,  'MarkerFaceColor','b')
plot3(x1ts, x2ts, yts, 'ro', 'MarkerSize',3,  'MarkerFaceColor','r')
hold off

%--------------------------------------------------------------------------
% Процесс адаптации системы нечёткого вывода
%---------------------------------------------
% НАСТРАИВАЕМЫЕ ПАРАМЕТРЫ (19 шт):
%    - весовые коэффициенты правил 2, 3, 4, 5, 6, 7  (6 шт.);
%    - коэф. конц.термов переменных x1, x2, y (3+3+3=9 шт.); *(у меня 3 терма у у)
%    - коорд.максимумв термов "средний" переменных x1, x2 (2 шт.);
%    - коорд.макс.терм. "сред." перем. y (1 шт.)
%-----------------
% Весовые коэффициенты правил
w0 = [1  1  1  1  1  1]-0.001;   % начальное приближение
wL = [0  0  0  0  0  0];         % нижняя граница
wU = [1  1  1  1  1  1];         % верхняя граница

% Коэффициенты конццентрации термов переменных
x1_s10 = fisMg.input(1).mf(1).params(1);	% исх. знач. для x1 "низкий"
x1_s20 = fisMg.input(1).mf(2).params(1);	%       -//-        "средний"	
x1_s30 = fisMg.input(1).mf(3).params(1);	%       -//-        "высокий"		

x2_s10 = fisMg.input(2).mf(1).params(1);	% исх. знач. для x2 "низкий"	
x2_s20 = fisMg.input(2).mf(2).params(1);	%       -//-        "средний"	
x2_s30 = fisMg.input(2).mf(3).params(1);	%       -//-        "высокий"	

y_s10 = fisMg.output(1).mf(1).params(1);	% исх.знач.для y "низкий"	
y_s20 = fisMg.output(1).mf(2).params(1);	%       -//-     "средний"	
y_s30 = fisMg.output(1).mf(3).params(1);	%       -//-     "высокий"		


x12ys0 = [x1_s10  x1_s20  x1_s30 ...    % объедин.цент.конц. в один вектор
         x2_s10  x2_s20  x2_s30 ...
         y_s10   y_s20   y_s30];
x12ysL = 0.7*x12ys0;    % нижняя граница = начальное приближение - 30%                      
x12ysU = 1.3*x12ys0;	% верхняя граница = начальное приближение + 30%
  
% коорд.максимумв некотор.термов входных и выходных переменных     
x1_c20 = fisMg.input(1).mf(2).params(2);	% исх. знач. для x1 "средний"
x2_c20 = fisMg.input(2).mf(2).params(2);	%    -//-        x2 "средний"	  
y_c20 = fisMg.output(1).mf(2).params(2);	%    -//-        y "средний"			
     
x12yc0 = [x1_c20  x2_c20  y_c20];

dx1 = 0.3*(max(x1)-min(x1));
dx2 = 0.3*(max(x2)-min(x2));
dy = 0.2*(max(max(y))-min(min(y)));
x12ycL = x12yc0 - [dx1 dx2 dy];       % нижняя граница                      
x12ycU = x12yc0 + [dx1 dx2 dy];       % верхняя граница

% Объединение настраиваемых параметров в один вектор 
ParamFis0 = [w0  x12ys0  x12yc0];       % начальное приближение
ParamFisL = [wL  x12ysL  x12ycL];       % нижняя граница
ParamFisU = [wU  x12ysU  x12ycU];       % верхняя граница

% Масштабир.настраив.параметров (демасштаб. в функц. F_changeFISmg)
% Msht~[{w:6}, {x:6}, {y:3}, {dx:2}, {dy:1}]
Msht = [1 1 1 1 1 1 1 1 1 1 1 1 0.1 0.1 0.1 1 1 0.1];
% Msht = [1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1];   % отсутствие масшт.парам.
ParamFis0 = ParamFis0 .* Msht;
ParamFisL = ParamFisL .* Msht;
ParamFisU = ParamFisU .* Msht;

%---------------------------------------------
% ПАРАМЕТРЫ ОПТИМИЗАЦИИ

optimset('fmincon')     % вывод структуры с инф.о парам. алгоритма оптим.  

% options = [];
options = optimset('Display', 'iter');      % вывод инф. на каждой итерации
options.MaxIter = 25;                       % максимальное число итераций
options.DiffMinChange = 0.0001;
options.DiffMaxChange = 0.2;
options.LargeScale = 'off';

%---------------------------------------------
% ОПТИМИЗАЦИЯ

[ParamFis_opt, sqrtFis, flag] = fmincon(@F_errFISmg, ParamFis0, [], [], [], [], ...
    ParamFisL, ParamFisU, [], options, fisMg, [x1ob, x2ob], yob, Msht);

fisMgOpt = F_changeFISmg(ParamFis_opt, fisMg, Msht);	% сист.нечёт.выв.после оптимиз.

% fuzzy(fisMgOpt)
% showfis(fisMgOpt)

%---------------------------------------------
% ПОСТРОЕНИЕ ГРАФИКА НЕЧЁТКОГО ОТОБРАЖЕНИЯ МАМДАНИ ПОСЛЕ АДАПТАЦИИ

yMgOpt = zeros(n, n);
for i = 1:n
    yMgOpt(i,:) = evalfis([x1; ones(size(x1))*x2(i)], fisMgOpt)';    
end  

%---------------------------------------------

h4 = figure(4);
set(h4,'Position',[540  350  520  410])
colormap('default')
surf(x1, x2, yMgOpt)
axis([-6     6 ...
      -6	6 ...
      -40   40]); 
view(-40,30)
xlabel('x_1');   ylabel('x_2');   zlabel('y');
title('Система нечёткого вывода Мамдани после адаптации') 

pause(2.5);               % пауза 2,5 с

colormap('white')     % 
hold on
plot3(x1ob, x2ob, yob, 'bs', 'MarkerSize',3,  'MarkerFaceColor','b')
plot3(x1ts, x2ts, yts, 'ro', 'MarkerSize',3,  'MarkerFaceColor','r')
hold off

%--------------------------------------------------------------------------
% Вычисление среднеквадратических значений ошибки нечёткой аппроксимации
%---------------------------------------------

% FIS Мамдани до оптимизации
ytsMg = evalfis([x1ts, x2ts], fisMg);                   % реакция FIS на тест.выборку
RMSE_Mg = sqrt(sum((yts-ytsMg).^2)/numel(yts));         % среднекв.знач.ошибки

% FIS Мамдани после оптимизации
ytsMgOpt = evalfis([x1ts, x2ts], fisMgOpt);             % реакция FIS на тест.выборку
RMSE_MgOpt = sqrt(sum((yts-ytsMgOpt).^2)/numel(yts));	% среднекв.знач.ошибки

disp(' ')
disp('Средние квадратические значения ошибки аппроксимации:')
disp(['  - до адаптации:     RMSE = ',  num2str(RMSE_Mg)])
disp(['  - после адаптации:  RMSE = ',  num2str(RMSE_MgOpt)])
disp(' ')

figure(2);          
xlabel(['x_1       RMSE = ',num2str(RMSE_Mg)]);
figure(4);          
xlabel(['x_1       RMSE = ',num2str(RMSE_MgOpt)]);

%---------------------------------------------
% close([h1 h2 h3 h4])


