function cost = optimize(alpha)
    assignin("alpha", alpha);
    sim("SMC_TwoLink.slxs");
    cost = ITAE(length_ITAE);

end

