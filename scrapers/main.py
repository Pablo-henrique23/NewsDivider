import multiprocessing
import subprocess

# Lista com os nomes dos scripts a executar
scripts = ['jp.py']#"antagonista.py", "diariocentrodomundo.py", "jp.py"]

def run_script(script_name):
    #print(f"[INFO] Iniciando {script_name.replace('scripts/','')}")
    subprocess.run(["python", script_name])
    #print(f"[INFO] Finalizou {script_name.replace('scripts/','')}")

if __name__ == "__main__":
    processes = []

    for i, script in enumerate(scripts):
        p = multiprocessing.Process(target=run_script, args=(f'scripts/{script}',))
        p.start()
        processes.append(p)

    # Espera todos terminarem
    for p in processes:
        p.join()

    #print("[INFO] Todos os scripts terminaram.")
