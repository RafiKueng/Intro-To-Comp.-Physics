figure
subplot(2,1,1)
hold on;
plot(dim10(:,2),dim10(:,7)-0.5,'r');
plot(dim15(:,2),dim15(:,7)-0.5,'g');
plot(dim20(:,2),dim20(:,7)-0.5,'b');
plot(dim25(:,2),dim25(:,7)-0.5,'r--');
plot(dim30(:,2),dim30(:,7)-0.5,'g--');
plot(dim35(:,2),dim35(:,7)-0.5,'b--');
plot(dim40(:,2),dim40(:,7)-0.5,'m');

legend('N=10','N=15','N=20','N=25','N=30','N=35','N=40')
title('Probability of spanning cluster')
xlabel('p');
ylabel('prob(spanning cluster)')
hold off;

p = dim10(:,7);
msk = p>0.1 & p < 0.9;
m1=mean([dim10(:,7),dim15(:,7),dim20(:,7)],2);
m2=mean([dim40(:,7),dim30(:,7),dim35(:,7)],2);
m = m1-m2;
xi = 0:.001:1; 
yi = interp1(p(msk),m(msk),xi,'nearest'); 

subplot(2,1,2)
hold on;
plot(dim10(:,2),m,'r');
%plot(xi,yi,'g');


%legend('N=10','N=15','N=20','N=25','N=30','N=35','N=40')
title('avg(dim<25) - avg(dim>25)')
xlabel('p');
ylabel('arb.')
hold off;