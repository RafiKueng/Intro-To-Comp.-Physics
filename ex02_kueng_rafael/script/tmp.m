figure;
subplot(3,2,1);
hold on;
plot(dim10(:,2),dim10(:,7),'r');
plot(dim15(:,2),dim15(:,7),'g');
plot(dim20(:,2),dim20(:,7),'b');
plot(dim25(:,2),dim25(:,7),'r--');
plot(dim30(:,2),dim30(:,7),'g--');
plot(dim35(:,2),dim35(:,7),'b--');
plot(dim40(:,2),dim40(:,7),'m');

legend('N=10','N=15','N=20','N=25','N=30','N=35','N=40')
title('Probability of spanning cluster')
xlabel('p');
ylabel('prob(spanning cluster)')
hold off;

subplot(3,2,3);
hold on;
plot(dim10(:,2),dim10(:,3),'r');
plot(dim15(:,2),dim15(:,3),'g');
plot(dim20(:,2),dim20(:,3),'b');
plot(dim25(:,2),dim25(:,3),'r--');
plot(dim30(:,2),dim30(:,3),'g--');
plot(dim35(:,2),dim35(:,3),'b--');
plot(dim40(:,2),dim40(:,3),'m');

%legend('N=10','N=15','N=20','N=25','N=30','N=35','N=40')
title('Average Timesteps the Fire lasted')
xlabel('p');
ylabel('avg. time (sim. steps)')
hold off;

subplot(3,2,5);
hold on;
plot(dim10(:,2),dim10(:,5),'r');
plot(dim15(:,2),dim15(:,5),'g');
plot(dim20(:,2),dim20(:,5),'b');
plot(dim25(:,2),dim25(:,5),'r--');
plot(dim30(:,2),dim30(:,5),'g--');
plot(dim35(:,2),dim35(:,5),'b--');
plot(dim40(:,2),dim40(:,5),'m');

%legend('N=10','N=15','N=20','N=25','N=30','N=35','N=40')
title('Average path length of spanning cluster path')
xlabel('p');
ylabel('avg. length (sim.units)')

subplot(3,2,4);
hold on;
plot(dim10(:,2),dim10(:,4),'r');
plot(dim15(:,2),dim15(:,4),'g');
plot(dim20(:,2),dim20(:,4),'b');
plot(dim25(:,2),dim25(:,4),'r--');
plot(dim30(:,2),dim30(:,4),'g--');
plot(dim35(:,2),dim35(:,4),'b--');
plot(dim40(:,2),dim40(:,4),'m');

%legend('N=10','N=15','N=20','N=25','N=30','N=35','N=40')
title('Average Timesteps the Fire lasted per Dimension')
xlabel('p');
ylabel('avg. time (sim. steps) / dim')
hold off;

subplot(3,2,6);
hold on;
plot(dim10(:,2),dim10(:,6),'r');
plot(dim15(:,2),dim15(:,6),'g');
plot(dim20(:,2),dim20(:,6),'b');
plot(dim25(:,2),dim25(:,6),'r--');
plot(dim30(:,2),dim30(:,6),'g--');
plot(dim35(:,2),dim35(:,6),'b--');
plot(dim40(:,2),dim40(:,6),'m');

%legend('N=10','N=15','N=20','N=25','N=30','N=35','N=40')
title('Average path length of spanning cluster path per dimension')
xlabel('p');
ylabel('avg. length (sim.units) / dim')