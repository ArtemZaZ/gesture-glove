clear all       % ������� ������ (leaving the workspace empty)
clc             % ������� ���������� ����  (Clear Command Window) 

n = 10;         % ���������� ����� �������������
angle_real = linspace(0, 90, n);
dR_Rm_real = [1 0.64 0.27 0.2 0.14 0.1 0.086 0.08 0.072 0.066];

fis = readfis('approximator.fis');     % �������� �������� �������� ����. � �����                   

angle_appr = evalfis(dR_Rm_real, fis);

%--------------------------------------------------------------------------
% ������� ��������� ������� ��������� ������
%---------------------------------------------
% ������������� ��������� (10 ��):
%    - ����. ����.������ ���������� x;
%    - �����.��������� ������ ���������� x;
%-----------------

% ������������ ������������� ������ ����������
x_s10 = fis.input(1).mf(1).params(1);	% 
x_s20 = fis.input(1).mf(2).params(1);	%       -//-        	
x_s30 = fis.input(1).mf(3).params(1);	%       -//-        	
x_s40 = fis.input(1).mf(4).params(1);	%       -//- 
x_s50 = fis.input(1).mf(5).params(1);	%       -//- 

x_s0 = [x_s10 x_s20 x_s30 x_s40 x_s50];
x_s0L = 0.3*x_s0;    % ������ ������� = ��������� ����������� - 30%                      
x_s0U = 1.3*x_s0;	% ������� ������� = ��������� ����������� + 30%

x_c10 = fis.input(1).mf(1).params(2);	% ���. ����. ��� x
x_c20 = fis.input(1).mf(2).params(2);	%       -//-        	
x_c30 = fis.input(1).mf(3).params(2);	%       -//-        	
x_c40 = fis.input(1).mf(4).params(2);	%       -//- 
x_c50 = fis.input(1).mf(5).params(2);	%       -//-

x_c0 = [x_c10  x_c20  x_c30 x_c40 x_c50];
dR = 0.3*(max(dR_Rm_real)-min(dR_Rm_real));
x_c0L = x_c0 - [dR dR dR dR dR];       % ������ �������                      
x_c0U = x_c0 + [dR dR dR dR dR];       % ������� �������

% ����������� ������������� ���������� � ���� ������ 
ParamFis0 = [x_s0  x_c0];       % ��������� �����������
ParamFisL = [x_s0L  x_c0L];       % ������ �������
ParamFisU = [x_s0U  x_c0U];       % ������� �������

% ���������.��������.���������� (���������. � �����. F_changeFISmg)
% Msht = [];
Msht = [1 1 1 1 1 1 1 1 1 1];   % ���������� �����.�����.
ParamFis0 = ParamFis0 .* Msht;
ParamFisL = ParamFisL .* Msht;
ParamFisU = ParamFisU .* Msht;
% ��������� �����������

optimset('fmincon')     % ����� ��������� � ���.� �����. ��������� �����.  

% options = [];
options = optimset('Display', 'iter');      % ����� ���. �� ������ ��������
options.MaxIter = 30;                       % ������������ ����� ��������
options.DiffMinChange = 0.0001;
options.DiffMaxChange = 0.2;
options.LargeScale = 'off';

%---------------------------------------------
% �����������

[ParamFis_opt, sqrtFis, flag] = fmincon(@errFIS, ParamFis0, [], [], [], [], ...
    ParamFisL, ParamFisU, [], options, fis, dR_Rm_real, angle_real', Msht);

fisOpt = changeFIS(ParamFis_opt, fis, Msht);	% ����.�����.���.����� �������.

% showfis(fisMgOpt)

%---------------------------------------------

angle_opt = evalfis(dR_Rm_real, fisOpt);

h1 = figure(1);          
colormap('white') 
hold on;
plot(dR_Rm_real, angle_real, 'LineWidth', 2);
plot(dR_Rm_real, angle_appr, 'LineWidth', 2);
plot(dR_Rm_real, angle_opt, 'LineWidth', 2);
legend("�������� �����������", "������ �����������", "�����������");
hold off
xlabel('\Delta{R/R_m}');   ylabel('\alpha, ����.');
title('��������� ������������� �����������')  

% fuzzy(fisOpt)
