clc;
clear;
close all;

D = sim('SMC_ThreeLink_Inverse');

plot(D.X_d(:,1),D.X_d(:,2),'k','linewidth',2)
axis([-2 2 -2 2])
grid on

for i = 1:30:size(D.tout,1)

    l1 = line([0 D.X1(i,1)],[0 D.X1(i,2)],'color' , 'r','linewidth',4);
    l2 = line([D.X1(i,1) D.X2(i,1)],[D.X1(i,2) D.X2(i,2)],'color' , 'r','linewidth',4);
    l3 = line([D.X2(i,1) D.X3(i,1)],[D.X2(i,2) D.X3(i,2)],'color' , 'r','linewidth',4);
    hold on
    plot(D.X3(i,1),D.X3(i,2),'.')
    hold on
    pause(0.005)

        if i~=15991
            delete(l1)
            delete(l2)
            delete(l3)
        end
        
end