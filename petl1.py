#import needed libraries
from imp import reload
import petl as etl, psycopg2 as pg, sys
from sqlalchemy import *

# handle characters outside of ascii
reload(sys)
sys.setdefaultencoding('utf8')

# declare connection properties within dictionary
dbCnxns = {'operations':'dbname=operations user=etl host=127.0.0.1',
'python':'dbname=python user=etl host=127.0.0.1',
'production':'dbname=production user=etl host=127.0.0.1'}

# set connections and cursors
sourceConn = pg.connect(dbCnxns['operations']) #grab value by referencing key dictionary
targetConn = pg.connect(dbCnxns['python']) #grab value by referencing key dictionary
sourceCursor = sourceConn.cursor()
targetCursor = targetConn.cursor()

# retrieve the names of the source tables to be copied
sourceCursor.execute("""select table_name from information_schema.columns where table_name in ('orders','returns') group by 1""")
sourceTables = sourceCursor.fetchall()

# iterate through table names to copy over
for t in sourceTables:
    targetCursor.execute("drop table if exists %s" % (t[0]))
    sourceDs = etl.fromdb(sourceConn, 'select * from %s' % (t[0]))
    etl.todb(sourceDs, targetConn, t[0], create=True, sample=10000)
