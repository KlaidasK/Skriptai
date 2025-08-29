#!/usr/bin/env php
#!php
<?php

// Funkcija, kuri surenka procesų informaciją iš Linux sistemos
function getProcesses($username = null) {
    // komandą ps su pasirinktinais stulpeliais (vartotojas, PID, CPU%, MEM%, ir kt.)
    $command = "ps -eo user,pid,%cpu,%mem,vsz,rss,tty,stat,start,time,cmd --no-headers";
    exec($command, $output);

    $rows = [];

    // stulpelių pavadinimai
    $header = ['USER', 'PID', '%CPU', '%MEM', 'VSZ', 'RSS', 'TTY', 'STAT', 'START', 'TIME', 'COMMAND'];
    $rows[] = $header;

    // Apdorojama kiekviena eilutė
    foreach ($output as $line) {
        // Skaldome eilutę į maksimum 11 dalių, nes komanda (COMMAND) gali turėti tarpus
        $parts = preg_split('/\s+/', $line, 11);

        // Jei eilutė neteisingo formato, praleidžiame
        if (count($parts) < 11) continue;

        // Jei nurodytas vartotojas, filtruojame procesus pagal jį
        if ($username !== null && stripos($parts[0], $username) === false) {
            continue;
        }

        // Pridedame apdorotą eilutę į rezultatą
        $rows[] = $parts;
    }

    return $rows; // Grąžiname surinktus duomenis
}

// Funkcija suformatuoja procesų duomenis į paprastą tekstą su tabais tarp laukų
function formatAsTxt($rows) {
    $lines = [];
    foreach ($rows as $row) {
        $lines[] = implode("\t", $row);
    }
    return implode(PHP_EOL, $lines);
}

// Funkcija suformuoja CSV formatą, kur reikšmės apsuptos kabutėmis
function formatAsCsv($rows) {
    $csv = '';
    foreach ($rows as $row) {
        // Apsaugome kabutes reikšmėse
        $escaped = array_map(function($cell) {
            return str_replace('"', '""', $cell);
        }, $row);
        $csv .= '"' . implode('","', $escaped) . '"' . PHP_EOL;
    }
    return $csv;
}

// Funkcija formuoja HTML lentelę su procesų duomenimis
function formatAsHtml($rows) {
    $html = "<table border='1' cellpadding='5' cellspacing='0'>\n";
    foreach ($rows as $index => $row) {
        $html .= "<tr>";
        foreach ($row as $cell) {
            // Apsaugome HTML specialius simbolius
            $cell = htmlspecialchars($cell, ENT_QUOTES);
            // Pirmoje eilutėje naudoja <th> (antraštės), kituose <td>
            $html .= $index === 0 ? "<th>$cell</th>" : "<td>$cell</td>";
        }
        $html .= "</tr>\n";
    }
    $html .= "</table>\n";
    return $html;
}

// Funkcija įrašo suformatuotą turinį į failą
function writeLog($format, $content) {
    $filename = __DIR__ . DIRECTORY_SEPARATOR . "process_log.$format";
    $success = @file_put_contents($filename, $content);
    if ($success === false) {
        echo "Klaida: nepavyko įrašyti log failo. Patikrinkite teises.\n";
        exit(1);
    }
    echo "Log failas sukurtas: $filename\n";
    return $filename;
}

// Nustatome numatytą formatą ir vartotoją
$format = 'txt';
$username = null;

// Jeigu nurodytas pirmas argumentas, nustatome formatą
if ($_SERVER['argc'] > 1) {
    $format = strtolower($_SERVER['argv'][1]);
    // Tikriname ar formatas yra vienas iš leidžiamų
    if (!in_array($format, ['txt', 'html', 'csv'])) {
        echo "Neteisingas formatas. Leidžiami: txt, html, csv\n";
        exit(1);
    }
}
// Jeigu nurodytas antras argumentas, nustatome vartotoją, pagal kurį filtruosime
if ($_SERVER['argc'] > 2) {
    $username = $_SERVER['argv'][2];
}

// Gauname procesų duomenis (filtruojame jei reikia)
$processes = getProcesses($username);
if (empty($processes) || count($processes) === 1) {
    echo "Procesų nerasta.\n";
    exit(0);
}

// Formatuojame išėjimą pagal pasirinktą formatą
switch ($format) {
    case 'html':
        $formatted = formatAsHtml($processes);
        break;
    case 'csv':
        $formatted = formatAsCsv($processes);
        break;
    default:
        $formatted = formatAsTxt($processes);
        break;
}

// Įrašome į log failą
$filename = writeLog($format, $formatted);

// Laukiame vartotojo paspaudimo, kad ištrintume failą ir išeitume
echo "Paspausk Enter, kad ištrintum log failą ir baigtum darbą...";
fgets(STDIN);

if (file_exists($filename)) {
    unlink($filename);
    echo "\nLog failas ištrintas. Baigiama.\n";
} else {
    echo "\nĮspėjimas: log failas nerastas trinimui.\n";
}
exit(0);