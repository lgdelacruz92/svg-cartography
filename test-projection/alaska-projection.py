

if __name__ == "__main__":
    state_file = open('state-fips.csv', 'r')
    state_file_lines = state_file.readlines()
    for line in state_file_lines:
        state_row_data = line.replace('\n','').split(',')
        fips = state_row_data[3] if len(state_row_data[3]) == 2 else f'0{state_row_data[3]}'
        print(fips, state_row_data[0])