from datetime import datetime, timezone


def convert_time_zone(date: float):
        """Convert time zone to local time.
        
        Parameters
        ----------
        date : UNIX format 
               The date to be changed to local time.     
        
        Returns
        -------
        local_datetime : datetime adjusted according to local time zone
        """
        utc_datetime = datetime.utcfromtimestamp(date)
        local_datetime = utc_datetime.replace(tzinfo=timezone.utc).astimezone(tz=None)
        local_datetime = local_datetime.strftime('%Y-%m-%d %H:%M:%S')
        
        return local_datetime


def get_dt_now():

        dt_now = datetime.now()

        return (
            dt_now.strftime("%Y-%m-%d")
            + "_"
            + dt_now.strftime("%H:%M:%S")
        )
