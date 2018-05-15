
url1 = "https://lk-test1.migcredit.ru/page35/"
url3 = "https://lk-test3.migcredit.ru/page35/"

test1_sql = 'mck-t-ucdb'
test3_sql = 'mck-t3-ucdb'

my_host = test1_sql
my_user = 'MGC\DShorokh'
my_password = 'Password80'
my_db = 'ACDB'

req = """
select top 1
ph.Number
from ACDB.dbo.ApplicationInfo a
left join ACDB.dbo.Participant p on a.UCDB_ID=p.UCDB_ID and p.Role='Borrower'
left join ACDB.dbo.NaturalPerson np on p.NaturalPersonID=np.id
left join ACDB.dbo.Phone ph on np.PhoneListID=ph.ListID
where 1=1
and ph.Type = 'Mobile'
and a.UCDB_ID = REPLACE
"""