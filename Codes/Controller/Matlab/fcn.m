function [U , s]= fcn(alpha,beta, theta , dtheta , e , de, ddthetad)


    L1 = 1; % m
    L2 = 1.2; % m
    
    Lc1 = .5; % m
    Lc2 = .6; % m
     
    m1 = 1; % Kg
    m2 = 2; % Kgkk
    
    I1 = 1/12 * m1 * L1^2;  %kg.N
    I2 = 1/12 * m2 * L2^2;  %kg.N

    g = 9.8; % m/s^2
   
    
    M11 = m1 * Lc1^2 + I1 + m2*(L1^2 + Lc2^2 + 2 * L1 * Lc2 * cos(theta(2))) + I2;
    M12 = m2 * L1 * Lc2 * cos(theta(2)) + m2 * Lc2^2 + I2;
    M22 = m2 * Lc2^2 + I2;
    M=[M11 M12;M12 M22];

    G1 = m1 * Lc1 * cos(theta(1)) + m2 * (Lc2 * cos(theta(1) + theta(2)) + L1 * cos(theta(1)));
    G2 = m2 * Lc2 * cos(theta(1) + theta(2));
    G=[G1*g;G2*g];
    
    F12 = m2 * L1 * Lc2 * sin(theta(2));
    C=[-F12*dtheta(2) -F12*(dtheta(1)+dtheta(2));F12*dtheta(1) 0];
  
    c = alpha* eye(2);
    ebs = beta * eye(2);
    
    
    s = de + c * e;
       
    s = de+ c*e + 5 * (e.^2);
    
   
    U = M * (ddthetad + c* de + ebs * sign(s)) + C * dtheta + G;
end
