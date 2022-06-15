from pathlib import Path
from  openpecha import github_utils

def pecha_publish(pecha_path):
    github_utils.github_publish(
        pecha_path,
        message="initial commit",
        not_includes=[],
        layers=[],
        org="Openpecha",
        token="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"
    )

if __name__=='__main__':
    pedurma_types = ['namsel_pedurma', 'derge_google_pedurma']
    for pedurma_type in pedurma_types:
        pecha_paths = list(Path(f'./pecha_opf/{pedurma_type}/').iterdir())
        pecha_paths.sort()
        for pecha_path in pecha_paths:
            pecha_path = Path(f"{pecha_path}")
            pecha_publish(pecha_path)
            print(f'published {pecha_path.stem} of {pedurma_type}')


# D1793x