clc;
clear;
close all;

D = sim('SMC_TwoLink_Inverse');

plot(D.X(:,1),D.X(:,2),'r','linewidth',2)
hold on
plot(D.X_d(:,1),D.X_d(:,2),'k','linewidth',2)
hold on
plot(D.X(1,1),D.X(1,2),'*','linewidth',4)
hold on
plot(D.X(end,1),D.X(end,2),'*','linewidth',4)