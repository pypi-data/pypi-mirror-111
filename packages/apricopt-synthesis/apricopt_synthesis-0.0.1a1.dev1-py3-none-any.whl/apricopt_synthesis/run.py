import apricopt.model.ObservableFunction

apricopt.model.ObservableFunction.function_names = dict(apricopt.model.ObservableFunction.function_names,
                                                        **user_function_names_synthesis)
apricopt.model.ObservableFunction.function_names = dict(apricopt.model.ObservableFunction.function_names,
                                                        **user_function_names_generation)

cli_args = get_command_line_arguments()

synthesis_model, treatment_model, \
    virtual_patients, initial_treatment, \
    exclude_from_initialization, \
    synthesis_horizon, treatment_horizon, \
    random_seed, sim_engine, solver, \
    solver_parameters, num_processes, \
    output_filename = parse_synthesis_config_file(cli_args.yaml)

outfile = output_filename if not cli_args.output else cli_args.output

best_x, best_value, \
    h_return, n_bb_evals, \
    nb_iters = synthesize_therapy(synthesis_model, treatment_model,
                                  virtual_patients, initial_treatment,
                                  exclude_from_initialization,
                                  synthesis_horizon, treatment_horizon,
                                  random_seed, sim_engine, solver,
                                  solver_parameters, num_processes)

VPs = []
for id, vp in virtual_patients.items():
    if len(VPs) < 1:
        vp['id'] = id
        VPs.append(vp)

dump_synthesis_result(synthesis_model, sim_engine, VPs[0], synthesis_horizon,
                      best_x, best_value, h_return, outfile)
