import click
from flask.cli import with_appcontext
from .models import Booking, Aplikasi
from app import db
import pandas as pd
from datetime import datetime

def init_app(app):
    app.cli.add_command(import_booking)

@click.command('import-booking')
@click.argument('file_name')
@with_appcontext
def import_booking(file_name):
    try:
        tablename = 'booking'
        df = pd.read_csv(file_name)
        db_tab_cols = pd.read_sql_table(tablename, con = db.engine).columns.tolist()
        df.columns = db_tab_cols[1:10]
        for row in df.itertuples():
            aplikasi = Aplikasi.query.filter_by(name=row.aplikasi_id).first()
            check_in = datetime.strptime(row.check_in_date , '%d/%m/%Y').date()
            check_out = datetime.strptime(row.check_out_date , '%d/%m/%Y').date()
            df.at[row.Index, 'check_in_date'] = str(check_in)
            df.at[row.Index, 'check_out_date'] = str(check_out)
            if (aplikasi):
                df.at[row.Index, 'aplikasi_id'] = aplikasi.id
            else:
                aplikasi = Aplikasi.query.filter_by(name='tunai').first()
                df.at[row.Index,'aplikasi_id'] = aplikasi.id
        df.to_sql(con=db.engine, index=False, name=tablename, if_exists='append')
    except Exception as err:
        print(err)
        db.session.rollback()
    finally:
        db.session.close()

