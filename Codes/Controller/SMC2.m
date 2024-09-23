clc;
clear;
close all;

D = sim('SMC_ThreeLink_Inverse');

plot(D.X3(:,1),D.X3(:,2),'r','linewidth',2)
hold on
plot(D.X_d(:,1),D.X_d(:,2),'k','linewidth',2)
hold on
plot(D.X3(1,1),D.X3(1,2),'*','linewidth',4)
hold on
plot(D.X3(end,1),D.X3(end,2),'*','linewidth',4)
grid on