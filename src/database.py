from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Vulnerability(Base):
    __tablename__ = 'vulnerabilities'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)

class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///vulnerabilities.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_vulnerabilities(self, vulnerabilities):
        session = self.Session()
        for vuln in vulnerabilities:
            vulnerability = Vulnerability(title=vuln['title'], description=vuln['description'])
            session.add(vulnerability)
        session.commit()
        session.close()
