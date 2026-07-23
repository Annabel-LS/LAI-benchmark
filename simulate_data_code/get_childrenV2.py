import random
#20250714,
#输入：基因文件，对应祖源文件, 生成几代，每代最大crossover次数
#输出：每代基因文件，每代祖源文件
#Q：每代生多少人？ 由get_child_count控制，
#Q：上一代人是否全用上？ 是的，写了代码，上一代人必须全部用上，因此下一代人数至少要是上一代的一半以上


# 输入和输出文件，<包含>标题列和标题行，但没有进行内存卡控制，可能会爆内存
def get_child_count(gen):
    """根据代数返回每代的孩子人数"""
    child_counts = {
        1: 20,  # 第一代9人
        2: 30,  # 第二代12人
        3: 40,  # 第三代18人
        4: 50,  # 第四代27人
        5: 60,  # 第五代39人
        6: 70,  # 第六代54人
        7: 80,  # 第七代72人
        8: 90  # 第八代93人
    }
    return child_counts.get(gen, 99)  # 第九代及以后100人

#确保上一代人至少被选中1次，且父母不是同一个人
def select_parents(num_individuals, childN):
    # 生成0到num_individuals-1的随机排列作为基础序列
    base_permutation = random.sample(range(num_individuals), num_individuals)

    # 初始化覆盖标记和未覆盖个体集合
    covered_individuals = set()
    uncovered = set(range(num_individuals))

    father_list = []
    mother_list = []

    # 第一阶段：确保每个个体至少出现一次
    for i in range(num_individuals):
        father_idx = base_permutation[i]
        covered_individuals.add(father_idx)
        if father_idx in uncovered:
            uncovered.remove(father_idx)

        # 选择与父亲不同的母亲
        mother_idx = random.choice([x for x in range(num_individuals) if x != father_idx])
        covered_individuals.add(mother_idx)
        if mother_idx in uncovered:
            uncovered.remove(mother_idx)

        father_list.append(father_idx)
        mother_list.append(mother_idx)

    # 第二阶段：随机选择剩余的父代对
    for i in range(childN - num_individuals):
        # 如果有未覆盖的个体，优先使用它们
        if uncovered:
            candidate = random.choice(list(uncovered))
            uncovered.remove(candidate)
            covered_individuals.add(candidate)
            father_idx = candidate
        else:
            father_idx = random.randint(0, num_individuals - 1)

        # 确保母亲与父亲不同
        mother_idx = random.randint(0, num_individuals - 1)
        while mother_idx == father_idx:
            mother_idx = random.randint(0, num_individuals - 1)

        father_list.append(father_idx)
        mother_list.append(mother_idx)

    return father_list, mother_list


def crossover_haplotypes(haplo1, haplo2, cross_points):
    """在指定交叉点同步交换两个单倍型"""
    if not cross_points:
        return haplo1.copy(), haplo2.copy()

    segments = [0] + cross_points + [len(haplo1)]
    new_haplo1, new_haplo2 = [], []

    for i in range(len(segments) - 1):
        start, end = segments[i], segments[i + 1]
        if i % 2 == 0:
            new_haplo1.extend(haplo1[start:end])
            new_haplo2.extend(haplo2[start:end])
        else:
            new_haplo1.extend(haplo2[start:end])
            new_haplo2.extend(haplo1[start:end])

    return new_haplo1, new_haplo2


def process_individual(data, ancestry, index, crossN, header_offset=2):
    """处理单个个体（关键修复：标题列偏移）"""
    # 样本数据从第3列开始（跳过ID和POS列）
    col_start = 2 * index + header_offset
    col1 = [row[col_start] for row in data]
    col2 = [row[col_start + 1] for row in data]

    # 祖源数据同样从第3列开始
    ance1 = [row[col_start] for row in ancestry]
    ance2 = [row[col_start + 1] for row in ancestry]

    # 预先生成共享交叉点
    length = len(col1)
    if crossN > 0 and length > 1:
        cross_points = sorted(random.sample(range(1, length), min(crossN, length - 1)))
    else:
        cross_points = []

    # 使用相同交叉点处理两组数据
    new_col1, new_col2 = crossover_haplotypes(col1, col2, cross_points)
    new_ance1, new_ance2 = crossover_haplotypes(ance1, ance2, cross_points)

    # 随机选择一条单倍型
    selected = random.choice([0, 1])
    return (new_col1 if selected == 0 else new_col2,
            new_ance1 if selected == 0 else new_ance2)


def generate_offspring(parent_geno, parent_ancestry, parent_ids, gen_index, childN, crossN):
    """生成一代后代（修复索引计算）"""
    # 计算实际个体数量（减去标题列）
    if not parent_geno or len(parent_geno[0]) < 2:
        raise ValueError("输入数据格式错误：缺少标题列")

    num_individuals = (len(parent_geno[0]) - 2) // 2  # 减去ID和POS列
    num_rows = len(parent_geno)

    # 准备输出数据
    child_geno = []
    child_ancestry = []
    child_ids = []  # 存储新生成的后代ID

    # 处理标题列（保留ID和POS）
    for i in range(num_rows):
        # 检查行长度是否足够
        if len(parent_geno[i]) < 2:
            raise IndexError(f"第{i + 1}行数据列数不足")

        child_geno_row = [parent_geno[i][0], parent_geno[i][1]]  # ID和POS
        child_ancestry_row = [parent_ancestry[i][0], parent_ancestry[i][1]]
        child_geno.append(child_geno_row)
        child_ancestry.append(child_ancestry_row)

    # 生成每个孩子
    father_indices, mother_indices = select_parents(num_individuals, childN)

    for child_index in range(childN):
        # 随机选择父母（在有效范围内）
        father_idx = father_indices[child_index]
        mother_idx = mother_indices[child_index]

        # 处理父亲,随机1~crossN数量的crossover
        father_geno, father_ance = process_individual(parent_geno, parent_ancestry, father_idx, random.randint(1, crossN))
        # 处理母亲,随机1~crossN数量的crossover
        mother_geno, mother_ance = process_individual(parent_geno, parent_ancestry, mother_idx, random.randint(1, crossN))

        # 生成孩子ID - 根据代数和父母信息创建
        if gen_index == 1:  # 第一代
            # 使用原始父母ID
            father_id = parent_ids[father_idx]
            mother_id = parent_ids[mother_idx]
            child_id = f"{child_index + 1:02d}_{father_id}_{mother_id}"
        else:  # 第二代及以上
            # 使用父母在上一代中的编号
            father_code = f"{father_idx + 1:02d}"
            mother_code = f"{mother_idx + 1:02d}"
            child_id = f"{child_index + 1:02d}_{father_code}_{mother_code}"

        child_ids.append(child_id)

        # 组合父母单倍型
        for i in range(num_rows):
            # 添加父亲和母亲的单倍型
            child_geno[i].append(father_geno[i])
            child_geno[i].append(mother_geno[i])
            child_ancestry[i].append(father_ance[i])
            child_ancestry[i].append(mother_ance[i])

    return child_geno, child_ancestry, child_ids


def save_generation(gen_data, gen_ancestry, gen_ids, gen_index):
    """保存一代数据到文件（修复标题行格式）"""
    prefix = f"{gen_index:02d}"

    # 创建标题行
    header_geno = ["ID", "POS"]
    header_ancestry = ["ID", "POS"]

    # 添加后代ID到标题行（每个ID对应两列）
    for child_id in gen_ids:
        header_geno.append(child_id + "_A")  # 添加单倍型后缀
        header_geno.append(child_id + "_B")
        header_ancestry.append(child_id + "_A")
        header_ancestry.append(child_id + "_B")

    # 写入基因型文件
    with open(f'{prefix}_geno.txt', 'w') as f:
        # 写入标题行
        f.write("\t".join(header_geno) + "\n")
        # 写入数据行
        for row in gen_data:
            f.write("\t".join(row) + "\n")

    # 写入祖源文件
    with open(f'{prefix}_ancestry.txt', 'w') as f:
        # 写入标题行
        f.write("\t".join(header_ancestry) + "\n")
        # 写入数据行
        for row in gen_ancestry:
            f.write("\t".join(row) + "\n")


def multi_generation_simulation(geno_file, ancestry_file, generationN, crossN):
    """多代遗传模拟主函数（增强健壮性）"""
    # 读取初始基因型数据
    with open(geno_file, 'r') as f:
        lines = f.readlines()
        if not lines:
            raise ValueError("基因型文件为空")

        # 第一行是标题行
        header = lines[0].strip().split()
        # 提取数据行（跳过标题行）并过滤空行
        parent_geno = [line.strip().split() for line in lines[1:] if line.strip()]

    # 读取初始祖源数据
    with open(ancestry_file, 'r') as f:
        lines = f.readlines()
        if not lines:
            raise ValueError("祖源文件为空")

        # 跳过标题行并过滤空行
        parent_ancestry = [line.strip().split() for line in lines[1:] if line.strip()]

    # 初始父母ID（从标题行提取，跳过ID和POS列）
    # 提取唯一父母ID（每两列对应一个个体）
    parent_ids = []
    for i in range(2, len(header), 2):  # 从第三列开始，每两列处理一次
        # 提取基础ID（去掉_A/_B后缀）
        base_id = header[i].split('_')[0]
        parent_ids.append(base_id)

    # 检查两个文件行数是否一致
    if len(parent_geno) != len(parent_ancestry):
        raise ValueError(f"基因型文件({len(parent_geno)}行)和祖源文件({len(parent_ancestry)}行)行数不一致！")

    # 检查每行数据列数是否一致
    for i in range(len(parent_geno)):
        if len(parent_geno[i]) != len(header):
            raise ValueError(f"基因型文件第{i + 2}行列数({len(parent_geno[i])})与标题行({len(header)})不一致")
        if len(parent_ancestry[i]) != len(header):
            raise ValueError(f"祖源文件第{i + 2}行列数({len(parent_ancestry[i])})与标题行({len(header)})不一致")

    # 保存始祖数据（0代）
    founder_geno = parent_geno.copy()
    founder_ancestry = parent_ancestry.copy()
    founder_ids = parent_ids.copy()

    # 初始化累积所有代的数据（从第一代开始）
    cumulative_geno = []
    cumulative_ancestry = []
    cumulative_ids = []

    # 生成多代
    for gen in range(1, generationN + 1):
        print(f"生成第 {gen} 代...")
        # 每一代孩子不一样
        childN = get_child_count(gen)

        # 确定父母数据
        if gen == 1:
            # 第一代由始祖生育
            parent_data_geno = founder_geno
            parent_data_ancestry = founder_ancestry
            parent_data_ids = founder_ids
        else:
            # 第二代及以后由累积的所有代数据生育
            parent_data_geno = cumulative_geno
            parent_data_ancestry = cumulative_ancestry
            parent_data_ids = cumulative_ids

        # 生成后代
        child_geno, child_ancestry, child_ids = generate_offspring(
            parent_data_geno, parent_data_ancestry, parent_data_ids, gen, childN, crossN
        )

        # 保存当前代
        save_generation(child_geno, child_ancestry, child_ids, gen)

        # 将新生成的后代添加到累积数据中
        if gen == 1:
            # 第一代：初始化累积数据
            cumulative_geno = child_geno.copy()
            cumulative_ancestry = child_ancestry.copy()
            cumulative_ids = child_ids.copy()
        else:
            # 后续代：添加到累积数据中
            for i in range(len(cumulative_geno)):
                # 添加新孩子的数据列
                cumulative_geno[i].extend(child_geno[i][2:])
                cumulative_ancestry[i].extend(child_ancestry[i][2:])

            # 更新累积ID列表
            cumulative_ids.extend(child_ids)

# 使用示例
if __name__ == "__main__":
    # 设置参数
    GEN_N = 100  # 生成3代
    CROSS_N = 3  # 最大交叉3次

    # 运行多代遗传模拟
    try:
        multi_generation_simulation(
            geno_file="/home/hxjs/Localancestry_test/test/simulat_data/10代模拟数据/原始文件/CHS_YRI_ID_NEW.txt",
            ancestry_file="/home/cbz/newdev/111/YRI_CHS.txt",
            generationN=GEN_N,
            crossN=CROSS_N
        )
        print(f"成功生成{GEN_N}代数据！文件命名格式为：01_geno.txt, 01_ancestry.txt, ...")
        print(f"标题行命名原则：")
        print(f"第一代：01_父原始ID_母原始ID (如01_HG01583_HG01586)")
        print(f"第二代：02_父编号_母编号 (如02_01_03)")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        print("可能原因：")
        print("1. 输入文件格式不符合要求")
        print("2. 文件行数或列数不一致")
        print("3. 文件内容缺失或格式错误")
