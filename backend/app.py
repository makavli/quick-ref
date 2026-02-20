from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

DATABASE = 'references.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE "references" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Add comprehensive sample data
        samples = [
            # Python
            ('List Comprehension', 'Python', 'squares = [x**2 for x in range(10)]', 'python'),
            ('Dictionary Comprehension', 'Python', 'squares_dict = {x: x**2 for x in range(5)}', 'python'),
            ('Try-Except Block', 'Python', 'try:\n    result = 10 / 0\nexcept ZeroDivisionError as e:\n    print(f"Error: {e}")', 'python'),
            ('Lambda Function', 'Python', 'square = lambda x: x ** 2\nprint(square(5))', 'python'),
            ('Map and Filter', 'Python', 'numbers = [1, 2, 3, 4, 5]\nsquared = list(map(lambda x: x**2, numbers))\nevens = list(filter(lambda x: x % 2 == 0, numbers))', 'python'),
            ('String Formatting', 'Python', 'name = "Alice"\nage = 30\nprint(f"Name: {name}, Age: {age}")\nprint("Name: {}, Age: {}".format(name, age))', 'python'),
            ('File I/O', 'Python', 'with open("file.txt", "r") as f:\n    content = f.read()\n    for line in f:\n        print(line.strip())', 'python'),
            ('Class Definition', 'Python', 'class Dog:\n    def __init__(self, name):\n        self.name = name\n    def bark(self):\n        print(f"{self.name} barks!")', 'python'),
            ('Virtual Environment', 'Python', 'python -m venv venv\nsource venv/bin/activate  # Linux/Mac\nvenv\\Scripts\\activate  # Windows', 'bash'),
            ('Pip Install Requirements', 'Python', 'pip install -r requirements.txt\npip freeze > requirements.txt', 'bash'),
            
            # Docker
            ('Docker Build', 'Docker', 'docker build -t myapp:1.0 .\ndocker build -t myapp:latest --no-cache .', 'bash'),
            ('Docker Run Interactive', 'Docker', 'docker run -it image_name\ndocker run -it --name container_name image_name /bin/bash', 'bash'),
            ('Docker Run with Ports', 'Docker', 'docker run -d -p 8080:80 --name webserver nginx', 'bash'),
            ('Docker Run with Volumes', 'Docker', 'docker run -v /host/path:/container/path image_name\ndocker run -v data:/data -v /code:/app image_name', 'bash'),
            ('Docker Environment Variables', 'Docker', 'docker run -e DATABASE_URL=postgresql://localhost -e DEBUG=true image_name', 'bash'),
            ('Docker Container Management', 'Docker', 'docker ps -a\ndocker stop container_id\ndocker start container_id\ndocker rm container_id', 'bash'),
            ('Docker Image Management', 'Docker', 'docker images\ndocker rmi image_id\ndocker tag image_id new_image_name:tag', 'bash'),
            ('Docker Logs', 'Docker', 'docker logs container_id\ndocker logs -f container_id  # follow logs\ndocker logs --tail 100 container_id', 'bash'),
            ('Docker Network', 'Docker', 'docker network create my_network\ndocker run --network my_network --name app1 image_name\ndocker run --network my_network --name app2 image_name', 'bash'),
            ('Docker Exec Command', 'Docker', 'docker exec -it container_id /bin/bash\ndocker exec container_id ls -la /app', 'bash'),
            ('Docker Compose Up', 'Docker', 'docker-compose up -d\ndocker-compose up --build\ndocker-compose down', 'bash'),
            ('Docker Compose Services', 'Docker', 'docker-compose ps\ndocker-compose logs -f service_name\ndocker-compose restart service_name', 'bash'),
            
            # Git
            ('Git Clone Repository', 'Git', 'git clone https://github.com/user/repo.git\ngit clone https://github.com/user/repo.git my_folder', 'bash'),
            ('Git Add and Commit', 'Git', 'git add .\ngit commit -m "Add new feature"\ngit commit -am "Update feature"', 'bash'),
            ('Git Push and Pull', 'Git', 'git push origin main\ngit pull origin develop\ngit fetch origin', 'bash'),
            ('Git Branch Management', 'Git', 'git branch\ngit branch new_branch\ngit checkout new_branch\ngit checkout -b feature/new-feature', 'bash'),
            ('Git Merge Branch', 'Git', 'git checkout main\ngit merge feature/new-feature\ngit merge --no-ff feature/new-feature', 'bash'),
            ('Git Rebase', 'Git', 'git rebase main\ngit rebase -i HEAD~3  # interactive rebase last 3 commits', 'bash'),
            ('Git Stash', 'Git', 'git stash\ngit stash list\ngit stash pop\ngit stash drop', 'bash'),
            ('Git Log and Show', 'Git', 'git log --oneline\ngit log --graph --all\ngit show commit_hash\ngit diff branch1 branch2', 'bash'),
            ('Git Tag', 'Git', 'git tag v1.0.0\ngit push origin v1.0.0\ngit tag -l\ngit tag -d v1.0.0', 'bash'),
            ('Git Reset and Revert', 'Git', 'git reset --soft HEAD~1\ngit reset --hard HEAD~1\ngit revert commit_hash', 'bash'),
            ('Git Remote', 'Git', 'git remote -v\ngit remote add upstream https://github.com/user/repo.git\ngit remote remove origin', 'bash'),
            ('Git Config', 'Git', 'git config user.name "Your Name"\ngit config user.email "your@email.com"\ngit config --global user.name "Name"', 'bash'),
            
            # YAML
            ('YAML List', 'YAML', '- item1\n- item2\n- item3', 'yaml'),
            ('YAML Dictionary', 'YAML', 'key1: value1\nkey2: value2\nkey3: value3', 'yaml'),
            ('YAML Nested Structure', 'YAML', 'parent:\n  child1: value1\n  child2: value2\n  nested:\n    deep: value', 'yaml'),
            ('YAML List of Objects', 'YAML', 'items:\n  - id: 1\n    name: Alice\n  - id: 2\n    name: Bob', 'yaml'),
            ('YAML Multiline String', 'YAML', 'description: |\n  This is a multiline\n  string that preserves\n  line breaks\nfold: >\n  This is folded\n  into a single line', 'yaml'),
            ('YAML Anchors and Aliases', 'YAML', 'defaults: &defaults\n  timeout: 30\n  retries: 3\nservice1:\n  <<: *defaults\n  name: Service1', 'yaml'),
            ('YAML Boolean and Null', 'YAML', 'enabled: true\ndisabled: false\nempty: null\nalso_null: ~', 'yaml'),
            
            # Kubernetes
            ('Kubernetes Deployment', 'Kubernetes', 'apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: my-app\nspec:\n  replicas: 3\n  selector:\n    matchLabels:\n      app: my-app\n  template:\n    metadata:\n      labels:\n        app: my-app\n    spec:\n      containers:\n      - name: app\n        image: my-app:1.0\n        ports:\n        - containerPort: 8080', 'yaml'),
            ('Kubernetes Service', 'Kubernetes', 'apiVersion: v1\nkind: Service\nmetadata:\n  name: my-service\nspec:\n  type: ClusterIP\n  selector:\n    app: my-app\n  ports:\n  - port: 80\n    targetPort: 8080', 'yaml'),
            ('Kubernetes Pod', 'Kubernetes', 'apiVersion: v1\nkind: Pod\nmetadata:\n  name: my-pod\nspec:\n  containers:\n  - name: app\n    image: nginx:latest\n    ports:\n    - containerPort: 80', 'yaml'),
            ('Kubernetes ConfigMap', 'Kubernetes', 'apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: app-config\ndata:\n  app.properties: |\n    debug=true\n    log.level=INFO', 'yaml'),
            ('Kubernetes Secret', 'Kubernetes', 'apiVersion: v1\nkind: Secret\nmetadata:\n  name: db-secret\ntype: Opaque\ndata:\n  username: dXNlcm5hbWU=\n  password: cGFzc3dvcmQ=', 'yaml'),
            ('Kubectl Apply', 'Kubernetes', 'kubectl apply -f deployment.yaml\nkubectl apply -f service.yaml\nkubectl apply -f configmap.yaml', 'bash'),
            ('Kubectl Get Resources', 'Kubernetes', 'kubectl get pods\nkubectl get services\nkubectl get deployments\nkubectl get all', 'bash'),
            ('Kubectl Describe', 'Kubernetes', 'kubectl describe pod pod_name\nkubectl describe service service_name\nkubectl describe node node_name', 'bash'),
            ('Kubectl Logs', 'Kubernetes', 'kubectl logs pod_name\nkubectl logs -f pod_name\nkubectl logs pod_name -c container_name', 'bash'),
            ('Kubectl Exec', 'Kubernetes', 'kubectl exec -it pod_name -- /bin/bash\nkubectl exec pod_name -- ls -la /app', 'bash'),
            
            # Terraform
            ('Terraform Provider Block', 'Terraform', 'terraform {\n  required_providers {\n    aws = {\n      source  = "hashicorp/aws"\n      version = "~> 5.0"\n    }\n  }\n}\n\nprovider "aws" {\n  region = "us-east-1"\n}', 'terraform'),
            ('Terraform AWS EC2', 'Terraform', 'resource "aws_instance" "web" {\n  ami           = "ami-0c55b159cbfafe1f0"\n  instance_type = "t2.micro"\n  tags = {\n    Name = "web-server"\n  }\n}', 'terraform'),
            ('Terraform Variables', 'Terraform', 'variable "instance_type" {\n  type    = string\n  default = "t2.micro"\n}\n\nvariable "tags" {\n  type = map(string)\n  default = {\n    Environment = "dev"\n  }\n}', 'terraform'),
            ('Terraform Output', 'Terraform', 'output "instance_id" {\n  value       = aws_instance.web.id\n  description = "The instance ID"\n}\n\noutput "public_ip" {\n  value = aws_instance.web.public_ip\n}', 'terraform'),
            ('Terraform Data Source', 'Terraform', 'data "aws_ami" "amazon_linux" {\n  most_recent = true\n  owners      = ["amazon"]\n  filter {\n    name   = "name"\n    values = ["amzn2-ami-hvm-*"]\n  }\n}', 'terraform'),
            ('Terraform Local', 'Terraform', 'locals {\n  environment = "production"\n  app_name    = "my-app"\n  common_tags = {\n    Environment = local.environment\n    Application = local.app_name\n  }\n}', 'terraform'),
            ('Terraform Init Plan Apply', 'Terraform', 'terraform init\nterraform plan -out=tfplan\nterraform apply tfplan', 'bash'),
            ('Terraform Destroy', 'Terraform', 'terraform destroy\nterraform destroy -auto-approve', 'bash'),
            ('Terraform State', 'Terraform', 'terraform state list\nterraform state show resource_type.resource_name\nterraform state rm resource_type.resource_name', 'bash'),
            
            # Ansible
            ('Ansible Playbook Structure', 'Ansible', '---\n- hosts: all\n  become: yes\n  tasks:\n    - name: Update packages\n      apt:\n        update_cache: yes\n    - name: Install nginx\n      apt:\n        name: nginx\n        state: present', 'yaml'),
            ('Ansible Install Package', 'Ansible', '- name: Install packages\n  apt:\n    name: "{{ item }}"\n    state: present\n  loop:\n    - git\n    - curl\n    - vim', 'yaml'),
            ('Ansible Service Management', 'Ansible', '- name: Start nginx\n  service:\n    name: nginx\n    state: started\n    enabled: yes', 'yaml'),
            ('Ansible Copy File', 'Ansible', '- name: Copy config file\n  copy:\n    src: /local/config.conf\n    dest: /etc/app/config.conf\n    mode: "0644"\n    owner: root\n    group: root', 'yaml'),
            ('Ansible Template', 'Ansible', '- name: Deploy template\n  template:\n    src: nginx.conf.j2\n    dest: /etc/nginx/nginx.conf\n    mode: "0644"\n  notify: restart nginx', 'yaml'),
            ('Ansible Conditionals', 'Ansible', '- name: Task with condition\n  apt:\n    name: nginx\n    state: present\n  when: ansible_os_family == "Debian"', 'yaml'),
            ('Ansible Variables', 'Ansible', '---\nvars:\n  app_name: myapp\n  app_version: 1.0\n  app_port: 8080\n\ntasks:\n  - debug:\n      msg: "{{ app_name }} version {{ app_version }}"', 'yaml'),
            ('Ansible Handlers', 'Ansible', '- name: Update nginx config\n  template:\n    src: nginx.conf.j2\n    dest: /etc/nginx/nginx.conf\n  notify: restart nginx\n\nhandlers:\n  - name: restart nginx\n    service:\n      name: nginx\n      state: restarted', 'yaml'),
            ('Ansible Inventory', 'Ansible', '[webservers]\nweb1.example.com\nweb2.example.com\n\n[databases]\ndb1.example.com\n\n[all:vars]\nansible_user=ubuntu\nansible_ssh_private_key_file=/home/user/.ssh/id_rsa', 'yaml'),
            ('Ansible Run Playbook', 'Ansible', 'ansible-playbook playbook.yml\nansible-playbook playbook.yml -i inventory.ini\nansible-playbook playbook.yml -e "var=value"', 'bash'),
        ]
        
        for title, category, content, lang in samples:
            cursor.execute('''
                INSERT INTO "references" (title, category, content, language)
                VALUES (?, ?, ?, ?)
            ''', (title, category, content, lang))
        
        conn.commit()
        conn.close()

@app.route('/api/references', methods=['GET'])
def get_references():
    search = request.args.get('search', '').lower()
    category = request.args.get('category', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM "references" WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (title LIKE ? OR content LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if category:
        query += ' AND category = ?'
        params.append(category)
    
    cursor.execute(query, params)
    refs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(refs)

@app.route('/api/references', methods=['POST'])
def create_reference():
    data = request.json
    
    if not data.get('title') or not data.get('content') or not data.get('category'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO "references" (title, category, content, language)
        VALUES (?, ?, ?, ?)
    ''', (data['title'], data['category'], data['content'], data.get('language', '')))
    
    conn.commit()
    ref_id = cursor.lastrowid
    conn.close()
    
    return jsonify({'id': ref_id, 'message': 'Reference created'}), 201

@app.route('/api/references/<int:ref_id>', methods=['GET'])
def get_reference(ref_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM "references" WHERE id = ?', (ref_id,))
    ref = cursor.fetchone()
    conn.close()
    
    if not ref:
        return jsonify({'error': 'Not found'}), 404
    
    return jsonify(dict(ref))

@app.route('/api/references/<int:ref_id>', methods=['PUT'])
def update_reference(ref_id):
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE "references" 
        SET title = ?, category = ?, content = ?, language = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (data.get('title'), data.get('category'), data.get('content'), 
          data.get('language', ''), ref_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Reference updated'})

@app.route('/api/references/<int:ref_id>', methods=['DELETE'])
def delete_reference(ref_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "references" WHERE id = ?', (ref_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Reference deleted'})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT category FROM "references" ORDER BY category')
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(categories)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path and os.path.exists(os.path.join('static', path)):
        return send_from_directory('static', path)
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
