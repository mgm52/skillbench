from simulation.simulator import Simulator

train_dataset, eval_dataset = ... # split by time

train_sim = Simulator(train_dataset)
eval_sim = Simulator(eval_dataset)

emu = TrueSkillEmulator(...)

train_sim.fit_emulator(emu, N)
eval_sim.evaluate_emulator(emu)