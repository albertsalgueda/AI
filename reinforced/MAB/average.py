#script to calculate an average on the fly.

count = 0
old_estimate = 0.0
while True:
    count += 1
    val = float(input('enter a number: '))
    current_estimate = old_estimate + (1/count)*(val-old_estimate)
    old_estimate = current_estimate
    print(f'current average: {current_estimate}')