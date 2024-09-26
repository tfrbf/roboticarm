% optimize_alpha.m
function optimize_alpha()
    % مقدار اولیه برای alpha
    initial_alpha = 1; 
     initial_beta = 1;

    % گزینه‌های بهینه‌سازی
    options = optimoptions('fminunc', 'Display', 'iter', 'Algorithm', 'quasi-newton');

    % اجرای بهینه‌سازی
    optimal_alpha = fminunc(@(alpha,beta) objective_alpha(alpha,beta), initial_alpha,initial_beta, options);

    % نمایش نتیجه
    fprintf('بهترین مقدار alpha: %.4f\n', optimal_alpha,optimal_beta);
end