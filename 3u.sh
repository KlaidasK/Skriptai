#!/bin/bash

# Tikrieji naudotojai: UID >= 1000 ir shell bash/sh
mapfile -t real_users < <(awk -F: '$3 >= 1000 && $7 ~ /bash|sh/ { print $1 }' /etc/passwd)

# Paimam naudotojo parametrą arba visi, jei nenurodytas
TARGET_USER="${1:-ALL}"
TARGET_ONLY=false
if [[ "$TARGET_USER" != "ALL" ]]; then
    TARGET_ONLY=true
fi

# Sukuriam laiko žymeklį ir kataloga
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M%S)
DATETIME="$DATE-$TIME"
LOG_DIR="user-process-logs-$DATETIME"
mkdir "$LOG_DIR"

# Procesai: naudotojas, PID, pavadinimas, CPU, RAM
mapfile -t process_list < <(ps -eo user:20,pid,comm,%cpu,%mem --no-headers)

# Log failų masyvas
declare -A log_paths

# Jei tik vienas naudotojas – tik jam log failas
if [[ "$TARGET_ONLY" == true ]]; then
    log_file="$LOG_DIR/${TARGET_USER}-process-log-$DATETIME.log"
    echo -e "Username: $TARGET_USER\nDate: $DATE\nTime: $(date +%H:%M:%S)\n" > "$log_file"
    log_paths["$TARGET_USER"]="$log_file"
else
    # Visiems tikriesiems naudotojams
    for u in "${real_users[@]}"; do
        log_paths["$u"]="$LOG_DIR/${u}-process-log-$DATETIME.log"
        echo -e "Username: $u\nDate: $DATE\nTime: $(date +%H:%M:%S)\n" > "${log_paths[$u]}"
    done
    # Log failas ne realiems naudotojams
    no_user_log="$LOG_DIR/no-user-process-log-$DATETIME.log"
    echo -e "Username: no-user\nDate: $DATE\nTime: $(date +%H:%M:%S)\n" > "$no_user_log"
fi

# Logai
for proc in "${process_list[@]}"; do
    user=$(echo "$proc" | awk '{print $1}')
    pid=$(echo "$proc" | awk '{print $2}')
    cmd=$(echo "$proc" | awk '{print $3}')
    cpu=$(echo "$proc" | awk '{print $4}')
    mem=$(echo "$proc" | awk '{print $5}')

    log_entry="Process Name: $cmd
PID: $pid
CPU Usage (%): $cpu
Memory Usage (%): $mem
--------------------------"

    if [[ "$TARGET_ONLY" == true ]]; then
        if [[ "$user" == "$TARGET_USER" ]]; then
            echo "$log_entry" >> "${log_paths[$TARGET_USER]}"
        fi
    else
        if [[ " ${real_users[*]} " == *" $user "* ]]; then
            echo "$log_entry" >> "${log_paths[$user]}"
        else
            echo "$log_entry" >> "$no_user_log"
        fi
    fi
done

echo "Logs stored in directory: $LOG_DIR"
echo ""

total_lines=0
for file in "$LOG_DIR"/*.log; do
    count=$(wc -l < "$file")
    echo "$(basename "$file") - $count lines"
    total_lines=$((total_lines + count))
done

echo ""
echo "Total lines in all log files: $total_lines"

# Pauzė prieš ištrynimą
read -p "Paspauskite Enter, kad ištrintumėte log failus ir baigtumėte..."

# Viskas ištrinama
rm -rf "$LOG_DIR"
echo "Log failai pašalinti. Skriptas baigtas."
