

##  Request for searching an account
req1 = """
select top 1
ta.Login,
ta.Password
from ACDB.dbo.tAuth ta
left join ACDB.dbo.StatusInfo s on s.UCDB_ID=ta.UCDB_ID
left join ACDB.dbo.Dict_PAD_AppStage st on st.AppStatus = s.Status
where 1=1
and s.Status = 'REPLACE'
and(st.ExpireHours - DATEDIFF(HOUR, s.Date, getdate()))>0"""

# Request for checking login
req2 = """
select * from ACDB.dbo.tAuth ta where ta.Login like 'REPLACE'
"""