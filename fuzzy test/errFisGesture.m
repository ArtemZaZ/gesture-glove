function errFIS = errFisGesture(param, FISiter, inputFIS, target, Msht)
% ������ ������ ��� ����� ���������� (param) �������� ������� FISiter

% ��������� ����� ���������� �������� �������
FISiter = changeFisGesture(param, FISiter, Msht);

% �������� �����:
outFIS = evalfis(inputFIS, FISiter);

% ������ ������:
errFIS = sqrt(sum((target-outFIS).^2)/numel(outFIS));	% ��������.����.������
