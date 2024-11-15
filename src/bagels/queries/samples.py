from pathlib import Path

import yaml

from bagels.models.account import Account
from bagels.models.database.app import db_engine
from bagels.models.person import Person
from bagels.models.record import Record
from bagels.models.record_template import RecordTemplate
from bagels.models.split import Split
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db_engine)


def create_sample_entries():
    yaml_path = Path(__file__).parent.parent / "static" / "sample_entries.yaml"

    with open(yaml_path, "r") as file:
        sample_entries = yaml.safe_load(file)

    session = Session()
    try:
        # Create accounts
        accounts = {}
        for account_data in sample_entries["accounts"]:
            account = Account(**account_data)
            session.add(account)
            session.flush()
            accounts[account.id] = account

        # Create people
        people = {}
        for person_data in sample_entries["people"]:
            person = Person(**person_data)
            session.add(person)
            session.flush()
            people[person.id] = person

        # Create records
        for record_data in sample_entries["records"]:
            # Handle splits if present
            splits_data = record_data.pop("splits", None)

            # Create record
            record = Record(**record_data)
            session.add(record)
            session.flush()

            # Create splits if any
            if splits_data:
                for split_data in splits_data:
                    split = Split(recordId=record.id, **split_data)
                    session.add(split)

        # Create record templates
        for template_data in sample_entries["record_templates"]:
            template = RecordTemplate(**template_data)
            session.add(template)

        session.commit()
    finally:
        session.close()
