compute_k(data, 0);
printf("Base solution: %lf\n", data->k);

double par2[15] = { -0.07097891397915604,0.09037968768574217,0.03953863835261531,0.004395573116284663,0.04214144415742476,0.04975525546955612,0.16313034585464473,0.0984049625571094,0.06165209798185289,0.08770363053852132,0.16436445032747424,0.050891948884650234,0.12236974326387334,0.237981027967441,0.19452103400974274 };
data->big_list = par2; 
compute_k(data, 0);		
printf("Eddie solution: %lf\n", data->k);
printf("Fields\n");
for(i=data->h_offset;i<data->n_params;i++) {
	printf("%lf ", data->big_list[i]);
}
printf("\n");

printf("Pairs\n");
for(i=0;i<data->h_offset;i++) {
	printf("%lf ", data->big_list[i]);
}
printf("\n\n");

simple_minimizer(data);

printf("Fields\n");
for(i=data->h_offset;i<data->n_params;i++) {
	printf("%lf ", data->big_list[i]);
}
printf("\n");

printf("Pairs\n");
for(i=0;i<data->h_offset;i++) {
	printf("%lf ", data->big_list[i]);
}
printf("\n");
