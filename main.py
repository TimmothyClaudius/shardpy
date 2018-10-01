import random
import numpy as np


def d(num):
    return random.randint(1, num)


def calc_hit(att, dmg, crit, was_crit, dodge, armor):
    if att > dodge + 10 or was_crit:
        return max(dmg + crit - armor, 0)
    elif att > dodge:
        return max(dmg - armor, 0)
    return None


def main():
    proficiency = [2, 3, 4, 5, 6]
    dice = [4,6,8,10,12]
    for prof in proficiency:
        ability = min(max(3, prof), 5)
        print("\nProficiency: {}".format(prof))
        for die in dice:
            unarmored = [0, [], 0, []]
            light = [0, [], 0, []]
            heavy = [0, [], 0, []]
            trials = 100
            for i in range(0, trials):
                att = d(20) + prof + ability
                was_crit = att - prof - ability == 20
                dmg = d(die) + ability
                crit = d(die)

                u_calc = calc_hit(att, dmg, crit, was_crit, 10+ability, 0)
                unarmored[1] += [u_calc] if u_calc is not None else [0]
                if u_calc is not None:
                    unarmored[2] += 1
                    unarmored[3] += [u_calc]

                l_calc = calc_hit(att, dmg, crit, was_crit, 10+ability+prof, 0)
                light[1] += [l_calc] if l_calc is not None else [0]
                if l_calc is not None:
                    light[2] += 1
                    light[3] += [l_calc]

                h_calc = calc_hit(att, dmg, crit, was_crit, 10+ability, prof)
                heavy[1] += [h_calc] if h_calc is not None else [0]
                if h_calc is not None:
                    heavy[2] += 1
                    heavy[3] += [h_calc]

            unarmored[1], light[1], heavy[1] = np.mean(unarmored[1]), np.mean(light[1]), np.mean(heavy[1])
            unarmored[2], light[2], heavy[2] = unarmored[2]/trials*100, light[2]/trials*100, heavy[2]/trials*100
            unarmored[3], light[3], heavy[3] = np.mean(unarmored[3]), np.mean(light[3]), np.mean(heavy[3])

            print('Damage Dice: d{:d}'.format(die))
            print('Unarmored Damage: {:0.2f}, Hit Rate: {:0.0f}%, Damage Per Hit: {:0.2f}'
                  .format(unarmored[1], unarmored[2], unarmored[3]))
            print('Light Armor Damage: {:0.2f}, Hit Rate: {:0.0f}%, Damage Per Hit: {:0.2f}'
                  .format(light[1], light[2], light[3]))
            print('Heavy Armor Damage: {:0.2f}, Hit Rate: {:0.0f}%, Damage Per Hit: {:0.2f}'
                  .format(heavy[1], heavy[2], heavy[3]))


main()