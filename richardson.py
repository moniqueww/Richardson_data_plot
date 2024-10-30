import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dados_original = pd.read_csv("/home/gruma-r/Documentos/16-17.txt")

ur = []
dv = []
t = []
v = []
p = []

for i in range(0,1396):
    dv.append(dados_original.iloc[i][9])
    ur.append(dados_original.iloc[i][6])
    t.append(dados_original.iloc[i][5])
    v.append(dados_original.iloc[i][8])
    p.append(dados_original.iloc[i][7])
    
horarios1 = pd.date_range('2023-06-17 00:00:00', '2023-06-17 11:20:00', freq='T')
horarios2 = pd.date_range('2023-06-17 12:05:00', '2023-06-17 23:59:00', freq='T')
horarios = horarios1.append(horarios2)


# Plotting the temperature and humidity on the same graph
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plotting the temperature
ax1.plot(horarios, t, marker='.', linestyle='-', color='tab:blue', label='Temperatura')
ax1.set_xlabel('Horário')
ax1.set_ylabel('Temperatura (°C)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True)
ax1.legend(loc='upper left')

# Creating a secondary y-axis for the humidity
ax2 = ax1.twinx()
ax2.plot(horarios, ur, marker='.', linestyle='-', color='tab:orange', label='Umidade Relativa')
ax2.set_ylabel('Umidade Relativa (%)', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')
ax2.legend(loc='upper right')

# Formatting the x-axis labels
plt.title('Dia 17 (horário local) - Temperatura do ar e Umidade Relativa')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Show the plot
plt.show()
#-------------------------------------------
# Plotting the wind speed and wind direction on the same graph
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plotting the temperature
ax1.plot(horarios, dv, marker='.', linestyle='-', color='tab:green', label='Direção do vento')
ax1.set_xlabel('Horário')
ax1.set_ylabel('Direção do vento (º)', color='tab:green')
ax1.tick_params(axis='y', labelcolor='tab:green')
ax1.grid(True)
ax1.legend(loc='upper left')

# Creating a secondary y-axis for the humidity
ax2 = ax1.twinx()
ax2.plot(horarios, v, marker='.', linestyle='-', color='tab:red', label='Velocidade do vento')
ax2.set_ylabel('Velocidade do vento (m/s)', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.legend(loc='upper right')

# Formatting the x-axis labels
plt.title('Dia 17 (horário local) - Direção e velocidade do vento')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Show the plot
plt.show()

#----------------------------------------NÚMERO DE RICHARDSON---------------------------------#
#CONSTANTES DA SONDAGEM
ctes_sondagem = {
    'pressao': [1000, 968, 955, 925],
    'altura': [219, 490, 602, 866],
    'sknt': [2.05778, 4.11556, 5.14444, 5.65889],
    'THTA': [284.1, 286.4, 286.4, 286.5]
}

#equação Ri
#MÉDIA THETA para 10 horas
theta_10horas = np.zeros((60, 4))
dtheta_10horas = np.zeros((60,4))
dz_10horas = np.zeros((60,4))
du_10horas = np.zeros((60,4))
Ri_10horas = np.zeros((60,4))

theta = []

for i in range(60):
    theta = t[600+i]*((1000/p[600+i])**0.28) + 273.15
    theta_10horas[i][0] = (theta + ctes_sondagem['THTA'][0])/2
    theta_10horas[i][1] = (theta + ctes_sondagem['THTA'][0] + ctes_sondagem['THTA'][1])/3
    theta_10horas[i][2] = (theta + ctes_sondagem['THTA'][0] + ctes_sondagem['THTA'][1] + ctes_sondagem['THTA'][2])/4
    theta_10horas[i][3] = (theta + ctes_sondagem['THTA'][0] + ctes_sondagem['THTA'][1] + ctes_sondagem['THTA'][2] + ctes_sondagem['THTA'][3])/5

#DELTA THETA para 10 horas
for i in range(60):
    theta = t[600+i]*((1000/p[600+i])**0.28) + 273.15
    dtheta_10horas[i][0] = ctes_sondagem['THTA'][0] - theta 
    dtheta_10horas[i][1] = ctes_sondagem['THTA'][1] - theta
    dtheta_10horas[i][2] = ctes_sondagem['THTA'][2] - theta
    dtheta_10horas[i][3] = ctes_sondagem['THTA'][3] - theta

#DELTA Z para 10 horas
z = 3
for i in range(60):
    dz_10horas[i][0] = ctes_sondagem['altura'][0] - z
    dz_10horas[i][1] = ctes_sondagem['altura'][1] - z
    dz_10horas[i][2] = ctes_sondagem['altura'][2] - z
    dz_10horas[i][3] = ctes_sondagem['altura'][3] - z

#DELTA U para 10 horas
for i in range(60):
    u = v[i+600]
    du_10horas[i][0] = ctes_sondagem['sknt'][0] - u
    du_10horas[i][1] = ctes_sondagem['sknt'][1] - u
    du_10horas[i][2] = ctes_sondagem['sknt'][2] - u
    du_10horas[i][3] = ctes_sondagem['sknt'][3] - u
    
#Ri
for i in range(60):
  Ri_10horas[i][0] = (9.8/theta_10horas[i][0])*((dtheta_10horas[i][0]*dz_10horas[0][0])/((du_10horas[i][0])**2))
  Ri_10horas[i][1] = (9.8/theta_10horas[i][1])*((dtheta_10horas[i][1]*dz_10horas[0][1])/((du_10horas[i][1])**2))
  Ri_10horas[i][2] = (9.8/theta_10horas[i][2])*((dtheta_10horas[i][2]*dz_10horas[0][2])/((du_10horas[i][2])**2))
  Ri_10horas[i][3] = (9.8/theta_10horas[i][3])*((dtheta_10horas[i][3]*dz_10horas[0][3])/((du_10horas[i][3])**2))

#plotar Ri 3 níveis
horario = pd.date_range('2023-06-17 10:00:00', '2023-06-17 10:59:00', freq='T')

plt.figure(figsize=(10, 6))
plt.plot(horario, Ri_10horas[:, 1], label='968 hPa')
plt.plot(horario, Ri_10horas[:, 2], label='955 hPa')
plt.plot(horario, Ri_10horas[:, 3], label='925 hPa')


plt.xlabel('Horário (local)')
plt.ylabel('Número de Richardson (Ri)')
plt.title('Dia 17 (horário local) - Número de Richardson (Ri) para 3 níveis de pressão')
plt.legend()
plt.grid(True)
plt.ylim(-6, 2) 
plt.show()