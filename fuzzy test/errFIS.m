function errFIS = errFIS(param, FISiter, inputFIS, target, Msht)
% Расчет ошибки при новых параметрах (param) нечеткой системы FISiter

% Установка новых параметров нечеткой системы
FISiter = changeFIS(param, FISiter, Msht);

% Нечеткий вывод:
outFIS = evalfis(inputFIS, FISiter);

% Расчет ошибки:
errFIS = sqrt(sum((target-outFIS).^2)/numel(outFIS));	% среднекв.знач.ошибки
