import os
import urllib.request

icons = {
    # Languages
    "python": "https://icon.icepanel.io/Technology/svg/Python.svg",
    "typescript": "https://icon.icepanel.io/Technology/svg/TypeScript.svg",
    "javascript": "https://icon.icepanel.io/Technology/svg/JavaScript.svg",
    "cplusplus": "https://icon.icepanel.io/Technology/svg/C%2B%2B-%28CPlusPlus%29.svg",
    "c": "https://icon.icepanel.io/Technology/svg/C.svg",
    "java": "https://icon.icepanel.io/Technology/svg/Java.svg",
    "html5": "https://icon.icepanel.io/Technology/svg/HTML5.svg",
    "css3": "https://icon.icepanel.io/Technology/svg/CSS3.svg",
    "bash": "https://icon.icepanel.io/Technology/svg/Bash.svg",

    # AI & ML
    "pytorch": "https://icon.icepanel.io/Technology/svg/PyTorch.svg",
    "tensorflow": "https://icon.icepanel.io/Technology/svg/TensorFlow.svg",
    "scikitlearn": "https://icon.icepanel.io/Technology/svg/scikit-learn.svg",
    "opencv": "https://icon.icepanel.io/Technology/svg/OpenCV.svg",
    "numpy": "https://icon.icepanel.io/Technology/svg/NumPy.svg",
    "pandas": "https://icon.icepanel.io/Technology/svg/Pandas.svg",
    "jupyter": "https://icon.icepanel.io/Technology/svg/Jupyter.svg",
    "anaconda": "https://icon.icepanel.io/Technology/svg/Anaconda.svg",
    "langchain": "https://cdn.simpleicons.org/langchain/1C3C3C",
    "huggingface": "https://cdn.simpleicons.org/huggingface",

    # Backend & APIs
    "fastapi": "https://icon.icepanel.io/Technology/svg/FastAPI.svg",
    "flask": "https://icon.icepanel.io/Technology/png-shadow-512/Flask.png",
    "streamlit": "https://icon.icepanel.io/Technology/svg/Streamlit.svg",
    "nodejs": "https://icon.icepanel.io/Technology/svg/Node.js.svg",
    "sqlalchemy": "https://icon.icepanel.io/Technology/svg/SQLAlchemy.svg",
    "graphql": "https://icon.icepanel.io/Technology/svg/GraphQL.svg",
    "openapi": "https://icon.icepanel.io/Technology/svg/OpenAPI.svg",

    # Frontend & UI
    "react": "https://icon.icepanel.io/Technology/svg/React.svg",
    "nextjs": "https://icon.icepanel.io/Technology/png-shadow-512/Next.js.png",
    "astro": "https://icon.icepanel.io/Technology/svg/Astro.svg",
    "tailwindcss": "https://icon.icepanel.io/Technology/svg/Tailwind-CSS.svg",
    "bootstrap": "https://icon.icepanel.io/Technology/svg/Bootstrap.svg",
    "redux": "https://icon.icepanel.io/Technology/svg/Redux.svg",
    "vite": "https://icon.icepanel.io/Technology/svg/Vite.js.svg",
    "figma": "https://icon.icepanel.io/Technology/svg/Figma.svg",
    "reactnative": "https://raw.githubusercontent.com/devicons/devicon/master/icons/reactnative/reactnative-original.svg",
    "expo": "https://raw.githubusercontent.com/devicons/devicon/master/icons/expo/expo-original.svg",

    # Databases
    "postgresql": "https://icon.icepanel.io/Technology/svg/PostgresSQL.svg",
    "mysql": "https://icon.icepanel.io/Technology/svg/MySQL.svg",
    "sqlite": "https://icon.icepanel.io/Technology/svg/SQLite.svg",
    "redis": "https://icon.icepanel.io/Technology/svg/Redis.svg",
    "mongodb": "https://icon.icepanel.io/Technology/svg/MongoDB.svg",

    # Cloud & DevOps
    "docker": "https://icon.icepanel.io/Technology/svg/Docker.svg",
    "kubernetes": "https://icon.icepanel.io/Technology/svg/Kubernetes.svg",
    "aws": "https://icon.icepanel.io/Technology/svg/AWS.svg",
    "githubactions": "https://icon.icepanel.io/Technology/svg/GitHub-Actions.svg",
    "nginx": "https://icon.icepanel.io/Technology/svg/NGINX.svg",
    "linux": "https://icon.icepanel.io/Technology/svg/Linux.svg",

    # Tools
    "git": "https://icon.icepanel.io/Technology/svg/Git.svg",
    "github": "https://icon.icepanel.io/Technology/png-shadow-512/GitHub.png",
    "vscode": "https://icon.icepanel.io/Technology/svg/Visual-Studio-Code-%28VS-Code%29.svg",
    "postman": "https://icon.icepanel.io/Technology/svg/Postman.svg",
}

os.makedirs('assets/icons', exist_ok=True)

success = 0
for name, url in icons.items():
    ext = ".png" if ".png" in url else ".svg"
    filepath = f"assets/icons/{name}{ext}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = urllib.request.urlopen(req, timeout=10).read()
        with open(filepath, 'wb') as f:
            f.write(data)
        success += 1
        print(f"Downloaded {name}{ext} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed {name} ({url}): {e}")

print(f"\nDone: {success}/{len(icons)} downloaded to assets/icons/")
