import random
import os
import matplotlib.pyplot as plt

def generate_page_references(num_references, num_pages):
    references = [random.randint(0, num_pages - 1) for _ in range(num_references)]
    
    # Define o nome do arquivo
    file_name = "page_references.txt"
    
    # Abre o arquivo no modo de adição (append)
    with open(file_name, "a") as file:
        # Adiciona um separador antes de cada nova execução
        file.write("\n--- Nova Execução ---\n")
        file.write(",".join(map(str, references)) + "\n")
    
    # Imprime o caminho completo do arquivo salvo
    print(f"Arquivo de referências salvo em: {os.path.abspath(file_name)}")
    
    return references

def fifo_simulation(page_references, num_frames):
    frames = []
    page_faults = 0
    
    for page in page_references:
        if page not in frames:
            if len(frames) < num_frames:
                frames.append(page)
            else:
                frames.pop(0)
                frames.append(page)
            page_faults += 1
    
    return page_faults

def aging_simulation(page_references, num_frames, aging_bits=8):
    frames = []
    ages = []
    page_faults = 0
    
    for page in page_references:
        if page in frames:
            idx = frames.index(page)
            ages[idx] = ages[idx] >> 1 | (1 << (aging_bits - 1))
        else:
            if len(frames) < num_frames:
                frames.append(page)
                ages.append(1 << (aging_bits - 1))
            else:
                min_age_idx = ages.index(min(ages))
                frames[min_age_idx] = page
                ages[min_age_idx] = 1 << (aging_bits - 1)
            page_faults += 1
        
        for i in range(len(ages)):
            ages[i] = ages[i] >> 1
    
    return page_faults

def simulate_and_plot(num_references, num_pages, max_frames):
    fifo_faults = []
    aging_faults = []
    frames_range = range(1, max_frames + 1)
    
    # Gera e salva as referências de páginas
    page_references = generate_page_references(num_references, num_pages)
    
    for num_frames in frames_range:
        fifo_faults.append(fifo_simulation(page_references, num_frames))
        aging_faults.append(aging_simulation(page_references, num_frames))
    
    plt.plot(frames_range, fifo_faults, label="FIFO")
    plt.plot(frames_range, aging_faults, label="Aging")
    plt.xlabel("Number of Frames")
    plt.ylabel("Page Faults per 1000 References")
    plt.title("Page Faults vs. Number of Frames")
    plt.legend()
    plt.show()

# Parâmetros de simulação
num_references = 1000
num_pages = 50
max_frames = 10

simulate_and_plot(num_references, num_pages, max_frames)
