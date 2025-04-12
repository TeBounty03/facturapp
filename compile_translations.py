import os
import polib

def compile_translations():
    # Chemins des fichiers
    base_dir = os.path.dirname(__file__)
    po_path = os.path.join(base_dir, 'locales', 'fr', 'LC_MESSAGES', 'fr.po')
    mo_path = os.path.join(base_dir, 'locales', 'fr', 'LC_MESSAGES', 'fr.mo')
    
    try:
        # Créer les répertoires si nécessaire
        os.makedirs(os.path.dirname(mo_path), exist_ok=True)
        
        # Charger et compiler le fichier PO
        po = polib.pofile(po_path)
        po.save_as_mofile(mo_path)
        
        print(f"Traduction compilée avec succès dans {mo_path}")
    except Exception as e:
        print(f"Erreur lors de la compilation : {str(e)}")
        print("Vérifiez que :")
        print("- Le fichier .po existe et est au bon format")
        print("- Vous avez les permissions d'écriture")

if __name__ == "__main__":
    compile_translations()