"""Database seeding script for QuantaLab."""
import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base
from app.core.security import get_password_hash
# Assume these models exist
from app.models.user import User, Role
from app.models.course import Course, Module, Lesson
from app.models.assessment import Assessment, Question, Choice
from app.models.circuit import Circuit
from app.models.progress import UserProgress

def seed_users(db: Session):
    print("Seeding users...")
    users_data = [
        {"email": "admin@quantalab.edu", "password": "password123", "full_name": "Admin User", "role": Role.ADMIN},
        {"email": "instructor@quantalab.edu", "password": "password123", "full_name": "Instructor User", "role": Role.INSTRUCTOR},
        {"email": "student@quantalab.edu", "password": "password123", "full_name": "Student User", "role": Role.STUDENT}
    ]
    
    for u_data in users_data:
        existing = db.query(User).filter(User.email == u_data["email"]).first()
        if not existing:
            hashed_pwd = get_password_hash(u_data["password"])
            user = User(
                email=u_data["email"],
                hashed_password=hashed_pwd,
                full_name=u_data["full_name"],
                role=u_data["role"]
            )
            db.add(user)
    db.commit()

def seed_courses(db: Session):
    print("Seeding courses...")
    
    # Check if exist
    if db.query(Course).first():
        return
        
    instructor = db.query(User).filter(User.role == Role.INSTRUCTOR).first()

    # Course 1: Quantum Computing Fundamentals
    c1 = Course(title="Quantum Computing Fundamentals", description="Learn the basics of quantum mechanics and quantum computing.", instructor_id=instructor.id)
    db.add(c1)
    db.commit()

    m1_1 = Module(title="Introduction to Quantum Mechanics", description="The physical principles.", course_id=c1.id, order=1)
    m1_2 = Module(title="Qubits and Quantum Gates", description="The building blocks of quantum information.", course_id=c1.id, order=2)
    m1_3 = Module(title="Quantum Circuits", description="Putting gates together.", course_id=c1.id, order=3)
    db.add_all([m1_1, m1_2, m1_3])
    db.commit()

    l1_1_1 = Lesson(title="What is Quantum Mechanics?", content="# Quantum Mechanics\n\nQuantum mechanics is a fundamental theory in physics that provides a description of the physical properties of nature at the scale of atoms and subatomic particles...", module_id=m1_1.id, order=1)
    l1_1_2 = Lesson(title="Superposition", content="# Superposition\n\nSuperposition is a principle of quantum mechanics that states that, much like waves in classical physics, any two (or more) quantum states can be added together...", module_id=m1_1.id, order=2)
    l1_1_3 = Lesson(title="Entanglement", content="# Quantum Entanglement\n\nEntanglement is a physical phenomenon that occurs when a group of particles are generated, interact, or share spatial proximity in a way such that the quantum state of each particle of the group cannot be described independently...", module_id=m1_1.id, order=3)
    
    l1_2_1 = Lesson(title="The Qubit", content="# Qubits\n\nThe qubit (quantum bit) is the basic unit of quantum information...", module_id=m1_2.id, order=1)
    l1_2_2 = Lesson(title="Pauli Gates (X, Y, Z)", content="# Pauli Gates\n\nThese are the fundamental single-qubit gates...", module_id=m1_2.id, order=2)
    l1_2_3 = Lesson(title="The Hadamard Gate", content="# The Hadamard Gate\n\nThe Hadamard gate (H-gate) is a fundamental quantum logic gate that creates superposition...", module_id=m1_2.id, order=3)
    
    l1_3_1 = Lesson(title="Multi-Qubit Gates", content="# Multi-Qubit Gates\n\nGates that act on multiple qubits like CNOT...", module_id=m1_3.id, order=1)
    l1_3_2 = Lesson(title="Building Simple Circuits", content="# Building Circuits\n\nCombining gates to form a quantum circuit...", module_id=m1_3.id, order=2)
    
    db.add_all([l1_1_1, l1_1_2, l1_1_3, l1_2_1, l1_2_2, l1_2_3, l1_3_1, l1_3_2])
    db.commit()

    # Course 2: Quantum Algorithms
    c2 = Course(title="Quantum Algorithms", description="Explore famous quantum algorithms.", instructor_id=instructor.id)
    db.add(c2)
    db.commit()

    m2_1 = Module(title="Deutsch-Jozsa Algorithm", description="Solving the constant vs balanced problem.", course_id=c2.id, order=1)
    m2_2 = Module(title="Grover's Search Algorithm", description="Searching unstructured databases.", course_id=c2.id, order=2)
    db.add_all([m2_1, m2_2])
    db.commit()

    l2_1_1 = Lesson(title="The Problem Statement", content="# The Deutsch-Jozsa Problem\n\nGiven a black-box boolean function, determine if it is constant or balanced...", module_id=m2_1.id, order=1)
    l2_1_2 = Lesson(title="The Algorithm", content="# The Deutsch-Jozsa Algorithm\n\nHow quantum parallelism solves it in one query...", module_id=m2_1.id, order=2)
    
    l2_2_1 = Lesson(title="Amplitude Amplification", content="# Amplitude Amplification\n\nThe core trick of Grover's algorithm...", module_id=m2_2.id, order=1)
    l2_2_2 = Lesson(title="Implementing Grover's Search", content="# Implementing Grover's\n\nStep-by-step circuit construction...", module_id=m2_2.id, order=2)

    db.add_all([l2_1_1, l2_1_2, l2_2_1, l2_2_2])
    db.commit()


def seed_assessments(db: Session):
    print("Seeding assessments...")
    if db.query(Assessment).first():
        return

    m1 = db.query(Module).filter(Module.title == "Introduction to Quantum Mechanics").first()
    
    a1 = Assessment(title="Quiz: Quantum Basics", module_id=m1.id)
    db.add(a1)
    db.commit()

    q1 = Question(assessment_id=a1.id, text="What is a qubit?", question_type="mcq")
    db.add(q1)
    db.commit()
    
    c1_1 = Choice(question_id=q1.id, text="A standard classical bit", is_correct=False)
    c1_2 = Choice(question_id=q1.id, text="A fundamental unit of quantum information", is_correct=True)
    c1_3 = Choice(question_id=q1.id, text="A type of quantum gate", is_correct=False)
    db.add_all([c1_1, c1_2, c1_3])
    db.commit()

def seed_circuits(db: Session):
    print("Seeding circuits...")
    if db.query(Circuit).first():
        return
        
    student = db.query(User).filter(User.role == Role.STUDENT).first()
    
    bell_qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q[0] -> c[0];\nmeasure q[1] -> c[1];'
    ghz_qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[3];\ncreg c[3];\nh q[0];\ncx q[0],q[1];\ncx q[1],q[2];\nmeasure q -> c;'
    
    c1 = Circuit(name="Bell State", description="A simple maximally entangled state.", qasm=bell_qasm, user_id=student.id)
    c2 = Circuit(name="GHZ State", description="A 3-qubit entangled state.", qasm=ghz_qasm, user_id=student.id)
    
    db.add_all([c1, c2])
    db.commit()

def seed_progress(db: Session):
    print("Seeding progress...")
    if db.query(UserProgress).first():
        return
        
    student = db.query(User).filter(User.role == Role.STUDENT).first()
    l1 = db.query(Lesson).first()
    
    p1 = UserProgress(user_id=student.id, lesson_id=l1.id, is_completed=True, score=None)
    db.add(p1)
    db.commit()

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_users(db)
        seed_courses(db)
        seed_assessments(db)
        seed_circuits(db)
        seed_progress(db)
        print("Seeding completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    main()
