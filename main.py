import time
import logging
import os
import glob
from datetime import datetime, timedelta
from backup import backup_world, conf

class BackupHelper:
    def __init__(self):
        self.backup_dir = conf["backup"]["output_dir"]
        log_dir = conf["auto"]["log_dir"]
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(log_dir, exist_ok=True)
        self.keep_days = conf["auto"]["keep_days"]

        log_file = os.path.join(log_dir, "backup_helper.log")  # 日志文件
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        self.interval = conf["auto"]["backup_interval_minutes"]
        self.backup_times_list = self.backup_times(self.interval)

    def backup_times(self, interval: int) -> list:
        """备份时间列表"""
        times = []
        # 从 00:00 开始
        for mins in range(0, 24 * 60, interval):
            hour = mins // 60
            minute = mins % 60
            times.append(f"{hour:02d}:{minute:02d}")
        return times

    def clean_expired_backups(self) -> int:
        """清理过期的备份"""
        now = datetime.now()
        deleted_count = 0
        archive_name = conf["backup"]["archive_name"]
        backups = glob.glob(os.path.join(self.backup_dir, f"{archive_name}_*.7z"))
        for file in backups:
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(file))  # 获取备份时间
                #
                if now - file_time > timedelta(days=self.keep_days):
                    os.remove(file)
                    logging.info(f"删除旧备份：{os.path.basename(file)}")
                    deleted_count += 1
            except Exception as e:
                logging.error(f"删除旧备份失败 {os.path.basename(file)}：{e}")
        return deleted_count

    def run_backup(self) -> None:
        """执行备份"""
        start_time = datetime.now()
        logging.info("开始自动备份...")
        success = backup_world(True)  # 静默模式
        duration = (datetime.now() - start_time).total_seconds()

        deleted_count = self.clean_expired_backups()
        if success:
            logging.info(f"备份成功，用时：{duration:.2f}秒")
            if deleted_count > 0:
                logging.info(f"已清理 {deleted_count} 个旧备份")
        else:
            logging.error(f"备份失败，用时：{duration:.2f}秒")

    def main(self) -> None:
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

        logging.info("自动备份守护进程启动")
        logging.info(f"备份间隔时长: {self.interval} 分钟")
        logging.info(f"所有备份时间点: {', '.join(self.backup_times_list)}")
        logging.info(f"备份保留策略: 最近 {self.keep_days} 天")
        logging.info("按 Ctrl+C 停止")

        try:
            while True:
                now = datetime.now().strftime("%H:%M")
                if now in self.backup_times_list:
                    self.run_backup()
                    # 避免同一分钟内重复执行
                    time.sleep(61)
                time.sleep(30)  # 每30秒检查一次时间
        except KeyboardInterrupt:
            logging.info("已停止备份守护进程")
        except Exception as e:
            logging.error(f"守护进程发生错误: {str(e)}")

if __name__ == "__main__":
    helper = BackupHelper()
    helper.main()