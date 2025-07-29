import multiprocessing
import subprocess

# Lista com os nomes dos scripts a executar
scripts = ["antagonista.py","diariocentrodomundo.py"]

def run_script(script_name, i):
    print(f"\033[32m[INFO] Iniciando {script_name.replace('scripts/','')}\033[3{i}m")
    subprocess.run(["python", script_name])
    print(f"\033[32m[INFO] Finalizou {script_name.replace('scripts/','')}\033[m")

if __name__ == "__main__":
    processes = []

    for i, script in enumerate(scripts):
        p = multiprocessing.Process(target=run_script, args=(f'scripts/{script}',i+3,))
        p.start()
        processes.append(p)

    # Espera todos terminarem
    for p in processes:
        p.join()

    print("[INFO] Todos os scripts terminaram.")
