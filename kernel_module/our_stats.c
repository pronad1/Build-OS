#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/seq_file.h>
#include <linux/mm.h>

static int our_show(struct seq_file *m, void *v) {
    unsigned long total_ram, free_ram, used_ram;
    struct sysinfo i;

    si_meminfo(&i);
    total_ram = i.totalram * PAGE_SIZE / (1024 * 1024);
    free_ram = i.freeram * PAGE_SIZE / (1024 * 1024);
    used_ram = total_ram - free_ram;

    seq_printf(m, "================================\n");
    seq_printf(m, "  My Custom OS Status\n");
    seq_printf(m, "================================\n");
    seq_printf(m, "Total RAM   : %lu MB\n", total_ram);
    seq_printf(m, "Used RAM    : %lu MB\n", used_ram);
    seq_printf(m, "Free RAM    : %lu MB\n", free_ram);
    seq_printf(m, "CPU Load    : (Simulated) 42%%\n");
    seq_printf(m, "================================\n");
    return 0;
}

static int our_open(struct inode *inode, struct file *file) {
    return single_open(file, our_show, NULL);
}

static const struct proc_ops our_ops = {
    .proc_open = our_open,
    .proc_read = seq_read,
};

static int __init our_init(void) {
    proc_create("our_stats", 0, NULL, &our_ops);
    printk(KERN_INFO "My OS Module: Loaded successfully!\n");
    return 0;
}

static void __exit our_exit(void) {
    remove_proc_entry("our_stats", NULL);
    printk(KERN_INFO "My OS Module: Unloaded successfully!\n");
}

module_init(our_init);
module_exit(our_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("Custom OS Status Module");
