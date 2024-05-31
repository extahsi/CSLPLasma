import logging
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.info("Database initialized and tables created")

    def save_vulnerabilities(self, vulnerabilities):
        session = self.Session()
        try:
            for vuln in vulnerabilities:
                vulnerability = Vulnerability(title=vuln['title'], description=vuln['description'])
                session.add(vulnerability)
            session.commit()
            logger.info("Vulnerabilities saved to database")
        except Exception as e:
            logger.error(f"Error saving vulnerabilities to database: {e}")
        finally:
            session.close()
