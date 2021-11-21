from logic import *

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

knowledge = And(
    Or(rain,hagrid),
    Not(rain)
)

print(model_check(knowledge, rain))


