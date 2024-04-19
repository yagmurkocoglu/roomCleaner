import random

# Hareket listesi
moves = ['left', 'no-op', 'right']

def main(p1, p2, p3):
    Agent_A_score = 0
    Agent_B_score = 0

    A = 'D'
    B = 'D'
    C = 'D'
    position = 'B'
    action = ''

    # Odalarda geçirilen süreyi ve kirlenme durumunu izleyen diziler
    time_spent_in_rooms = {'A': 0, 'B': 0, 'C': 0}
    room_states = {'A': A, 'B': B, 'C': C}
    contamination_counts = {'A': 0, 'B': 0, 'C': 0}

    with open('a.txt', 'w') as Agent_A, open('b.txt', 'w') as Agent_B:
        for time_step in range(1000):
            Agent_A.write(f'{position}, {A}, {B}, {C}\n')
            Agent_B.write(f'{position}, {A}, {B}, {C}\n')

            # Ajanın hareket seçimi
            if position == 'B':
                if B == 'D':
                    action = 'suck'
                else:
                    action = random.choice(moves)
                if action == 'suck':
                    B = 'C'
                    contamination_counts['B'] += 1
                elif action == 'left':
                    position = 'A'
                    Agent_B_score -= 0.5
                elif action == 'right':
                    position = 'C'
                    Agent_B_score -= 0.5

            elif position == 'A':
                if A == 'D':
                    action = 'suck'
                else:
                    action = random.choice(moves)
                if action == 'suck':
                    A = 'C'
                    contamination_counts['A'] += 1
                elif action == 'right':
                    position = 'B'
                    Agent_B_score -= 0.5
            else:
                if C == 'D':
                    action = 'suck'
                else:
                    action = random.choice(moves)
                if action == 'suck':
                    C = 'C'
                    contamination_counts['C'] += 1
                elif action == 'left':
                    position = 'B'
                    Agent_B_score -= 0.5

            # Puan güncellemeleri
            def update_scores(agent_a_score, agent_b_score, room_states):
                for room_state in room_states.values():
                    if room_state == 'C':
                        agent_a_score += 1
                        agent_b_score += 1
                return agent_a_score, agent_b_score

            Agent_A_score, Agent_B_score = update_scores(Agent_A_score, Agent_B_score, room_states)

            # İşlem ve durumları dosyaya yazma
            def write_to_file(agent_file, action, position, A, B, C, agent_score):
                agent_file.write(action + '\n')
                agent_file.write(f'{position}, {A}, {B}, {C}\n')
                agent_file.write(str(agent_score) + '\n')

            write_to_file(Agent_A, action, position, A, B, C, Agent_A_score)
            write_to_file(Agent_B, action, position, A, B, C, Agent_B_score)

            # Odaların durum güncellemeleri
            def update_room_states(room_state, probability):
                if room_state == 'C' and random.random() <= probability:
                    return 'D'
                return room_state

            # Odaların durum güncellemeleri ve geçirilen süreyi artırma
            A = update_room_states(A, p1)
            B = update_room_states(B, p2)
            C = update_room_states(C, p3)

            time_spent_in_rooms[position] += 1

            # Belirli bir iterasyon sonra ajanın kararını güncelleme
            if time_step > 100:
                max_time_spent_room = max(time_spent_in_rooms, key=time_spent_in_rooms.get)
                position = max_time_spent_room

    print("Training completed!")

    # İlk yüz iterasyonda kirlenme miktarını konsolda gösterme
    print("\nContamination counts in the first 100 iterations:")
    for room, count in contamination_counts.items():
        print(f"Room {room}: {count} contaminations")

if __name__ == '__main__':
    pA = float(input("Determine the probability of contamination in room A between 0 and 1: "))
    pB = float(input("Determine the probability of contamination in room B between 0 and 1: "))
    pC = float(input("Determine the probability of contamination in room C between 0 and 1: "))
    main(pA, pB, pC)

    # a.txt ve b.txt dosyalarını okuma modunda açma
    with open('a.txt', 'r') as Agent_A, open('b.txt', 'r') as Agent_B:
        # a.txt ve b.txt dosyalarının son satırlarını almak için readlines() metodunu kullanma
        last_line_A = Agent_A.readlines()[-1]
        last_line_B = Agent_B.readlines()[-1]

        # Son satırları konsola yazdırma
        print("\nAgent A score: " + last_line_A)
        print("Agent B score: " + last_line_B)
